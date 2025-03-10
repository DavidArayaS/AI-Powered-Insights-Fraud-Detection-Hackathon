from pyspark.sql.functions import (
    col, when, regexp_extract, regexp_replace, lit, split, explode, trim,
    row_number, monotonically_increasing_id, concat
)
from pyspark.sql.window import Window

# ---------------------------------------------------------------------------
# STEP 1: READ THE JSON DATA (which has analyzeResult.content)
# ---------------------------------------------------------------------------
df = spark.read.json("Files/financial")


df = df.selectExpr("analyzeResult.content AS Content")

# ---------------------------------------------------------------------------
# STEP 2: CLASSIFY DOCUMENTS AS 'Loan' OR 'Investment'
# ---------------------------------------------------------------------------
df_classified = (
    df
    .withColumn(
        "DocumentType",
        when(col("Content").rlike("(?i)Investment Portfolio Statement"), "Investment")
        .when(col("Content").rlike("(?i)Loan Application & Credit Report"), "Loan")
        .otherwise("Unknown")
    )
)

df_filtered = df_classified.filter(col("DocumentType").isin("Investment", "Loan"))

# ---------------------------------------------------------------------------
# STEP 3: EXTRACT COMMON FIELDS (Email, AddressID, plus actual Address text)
# ---------------------------------------------------------------------------

df_common = (
    df_filtered
    # Parse Email
    .withColumn("Email", regexp_extract(col("Content"), r"Email:\s*(\S+@\S+)", 1))

    # Parse "AddressID: X"
    .withColumn("AddressID", regexp_extract(col("Content"), r"AddressID:\s*([^\n]+)", 1))

    # Parse the actual Address line, e.g. "Address: 2369 Brown St, FL 72721"
    .withColumn("Address", regexp_extract(col("Content"), r"Address:\s*([^\n]+)", 1))
)

df_invest = (
    df_common
    .filter(col("DocumentType") == "Investment")
    .withColumn("ClientID", regexp_extract(col("Content"), r"ClientID:\s*([^\n]+)", 1))
    .withColumn("ClientName", regexp_extract(col("Content"), r"Client:\s*([^\n]+)", 1))
    .select("Content", "DocumentType", "ClientID", "ClientName", "Email", "AddressID", "Address")
)

# We'll split the entire Content by newline, explode into multiple rows,
# then filter only lines that match typical investment lines: Stocks, Bonds, ETFs, etc.
df_invest_exploded = (
    df_invest
    .withColumn("Line", explode(split(col("Content"), "\n")))
    .filter(col("Line").rlike("(?i)(Stocks|Bonds|ETFs|Mutual Funds|Commodities|Real Estate)"))
)

# Now parse the typical pattern: "<Type>: $<Value> | Return: X% | Risk: Y"
df_invest_parsed = (
    df_invest_exploded
    .withColumn("InvestmentType", regexp_extract(col("Line"), r"^(.*?)\s*:", 1))
    .withColumn("Value", regexp_replace(regexp_extract(col("Line"), r"\$(\S+)", 1), "%", "").cast("double"))
    .withColumn("Return", regexp_replace(regexp_extract(col("Line"), r"Return:\s*([-\d\.%]+)", 1), "%", "").cast("double"))
    .withColumn("Risk",   regexp_extract(col("Line"), r"Risk:\s*([A-Za-z]+)", 1))
    .select(
        "DocumentType", "ClientID", "ClientName", "Email", "AddressID", "Address",
        "InvestmentType", "Value", "Return", "Risk"
    )
)

# We'll add the Loan-only columns as null, so we can union with the Loan docs
df_invest_final = (
    df_invest_parsed
    .withColumn("ApplicantID",      lit(None).cast("string"))
    .withColumn("ApplicantName",    lit(None).cast("string"))
    .withColumn("AnnualIncome",     lit(None).cast("double"))
    .withColumn("CreditScore",      lit(None).cast("int"))
    .withColumn("RequestedAmount",  lit(None).cast("double"))
    .withColumn("ApprovedAmount",   lit(None).cast("double"))
    .withColumn("ApprovalStatus",   lit(None).cast("string"))
)

# ---------------------------------------------------------------------------
# STEP 4b: PROCESS LOAN DOCUMENTS
#         We parse ApplicantID, ApplicantName, plus typical loan fields.
# ---------------------------------------------------------------------------
df_loan = (
    df_common
    .filter(col("DocumentType") == "Loan")
    .withColumn("ApplicantID", regexp_extract(col("Content"), r"ApplicantID:\s*([^\n]+)", 1))
    .withColumn("ApplicantName", regexp_extract(col("Content"), r"Applicant:\s*([^\n]+)", 1))

    .withColumn("AnnualIncome",      regexp_extract(col("Content"), r"Annual Income:\s*\$(\S+)", 1).cast("double"))
    .withColumn("CreditScore",       regexp_extract(col("Content"), r"Credit Score:\s*(\d+)", 1).cast("int"))
    .withColumn("RequestedAmount",   regexp_extract(col("Content"), r"Requested Amount:\s*\$(\S+)", 1).cast("double"))
    .withColumn("ApprovedAmount",    regexp_extract(col("Content"), r"Approved Amount:\s*\$(\S+)", 1).cast("double"))
    .withColumn("ApprovalStatus",    regexp_extract(col("Content"), r"Approval Status:\s*([^\n]+)", 1))
    .select(
        "Content", "DocumentType", "ApplicantID", "ApplicantName", "Email", "AddressID", "Address",
        "AnnualIncome", "CreditScore", "RequestedAmount", "ApprovedAmount", "ApprovalStatus"
    )
)

df_loan_final = (
    df_loan
    .withColumn("ClientID",        lit(None).cast("string"))
    .withColumn("ClientName",      lit(None).cast("string"))
    .withColumn("InvestmentType",  lit(None).cast("string"))
    .withColumn("Value",           lit(None).cast("double"))
    .withColumn("Return",          lit(None).cast("double"))
    .withColumn("Risk",            lit(None).cast("string"))
)

# ---------------------------------------------------------------------------
# STEP 5: UNION INVESTMENT + LOAN INTO ONE FACT TABLE, REMOVE RAW Content
# ---------------------------------------------------------------------------
df_union = (
    df_invest_final
    .unionByName(df_loan_final, allowMissingColumns=True)
    .drop("Content")
)


df_renamed = (
    df_union
    .withColumnRenamed("Value", "Value_Dollar")
    .withColumnRenamed("Return", "Return_Percentage")
    .withColumnRenamed("AnnualIncome", "AnnualIncome_Dollar")
    .withColumnRenamed("RequestedAmount", "RequestedAmount_Dollar")
    .withColumnRenamed("ApprovedAmount", "ApprovedAmount_Dollar")
)

df_extended = (
    df_renamed
    .withColumn("NumberOfDependents", lit(None).cast("int"))
    .withColumn("YearsOfBeingCustomer", lit(None).cast("int"))
)

# ---------------------------------------------------------------------------
# STEP 6: ASSIGN UNIQUE IDs WHERE MISSING
#         (If ApplicantID, ClientID, or AddressID is null/empty,
#          generate a new one. NOTE each row gets a new ID if blank!)
# ---------------------------------------------------------------------------
windowApplicant = Window.orderBy(monotonically_increasing_id())
df_stepA = df_extended.withColumn(
    "ApplicantID",
    when(
        (col("ApplicantID").isNull()) | (col("ApplicantID") == ""),
        concat(lit("APP-"), row_number().over(windowApplicant))
    ).otherwise(col("ApplicantID"))
)

windowClient = Window.orderBy(monotonically_increasing_id())
df_stepB = df_stepA.withColumn(
    "ClientID",
    when(
        (col("ClientID").isNull()) | (col("ClientID") == ""),
        concat(lit("CLI-"), row_number().over(windowClient))
    ).otherwise(col("ClientID"))
)

windowAddress = Window.orderBy(monotonically_increasing_id())
df_final_ids = df_stepB.withColumn(
    "AddressID",
    when(
        (col("AddressID").isNull()) | (col("AddressID") == ""),
        concat(lit("ADDR-"), row_number().over(windowAddress))
    ).otherwise(col("AddressID"))
)

# ---------------------------------------------------------------------------
# STEP 7: WRITE TO A SINGLE DELTA TABLE
# ---------------------------------------------------------------------------
df_final_ids.write.format("delta").mode("overwrite").saveAsTable("FactFinancialTable")

print("✅ Done! Created 'FactFinancialTable' with numeric columns, renamed fields, and new int columns!")