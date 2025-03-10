# 📖 Solution to Challenge 5: Creating a Power BI Report from Financial Data in Microsoft Fabric  

---

## 🔹 Objective  
This guide will walk you through the entire process of extracting, transforming, and visualizing financial data using **Microsoft Fabric, Lakehouse, and Power BI**.

✅ Store and process financial data in **Fabric Lakehouse**  
✅ Run a **Notebook (PySpark) to transform data**  
✅ Create a **Semantic Model**  
✅ Automatically generate a **Power BI report**  

---

## 🚀 Step 1: Ensure Your Data is in Fabric Lakehouse  

💡 **Before proceeding, make sure** that your **financial data (JSON files)** are already uploaded to Fabric Lakehouse under `Files/json`.  

### 1️⃣ Verify Data Storage in Fabric Lakehouse  
1. Open **Microsoft Fabric**  
2. Navigate to your **Lakehouse workspace**  
3. Under the **Files** section, confirm the presence of `yourfolder` folder  
4. Ensure it contains **analyzed JSON files**  

✅ **Outcome**: Your JSON files are now stored in Fabric Lakehouse.  

---

## 🚀 Step 2: Run the PySpark Notebook to Transform Data  

💡 **Why?** The raw JSON data must be structured into a **relational format** before it can be used in Power BI.  

### 1️⃣ Open a Fabric Notebook  

1. In **Fabric**, go to your **Lakehouse workspace**  
2. Click **+ New** → **Notebook**  
3. Select **PySpark** as the language  

### 2️⃣ Copy & Paste the PySpark Code 

**(Financial Data)**

```python

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


```


### 3️⃣ Run the Notebook  
- Click **Run All** to execute the script  
- Wait for the process to complete  

✅ **Outcome**: A new table **FactFinancialTable** is now available in your **Fabric Lakehouse**.  

---
## 🚀 Step 3: Create the Lookup or Dimension Tables

1. Use the Excel files provided with your **Data Source Folder**
2. Open your Lakehose
3. Click **Get data**
4. Select **New Dataflow Gen2**
5. Select the **Enter Data** Option
6. Create a table for each of the Excel files using their content
7. **Publish** the tables, they should not be under Tables/ in your Lakehouse

---

## 🚀 Step 4: Create a Semantic Model  

💡 **Why?** The semantic model allows **Power BI** to interact with your **Fabric data**.  

### 1️⃣ Create a New Semantic Model  
1. Go to **Microsoft Fabric**  
2. Click open your Lakehouse and **Click → **Semantic Model**  
3. Name it **Financial-Semantic-Model**  


### 2️⃣ Select Your Financial Tables
1. In the **Select tables** section, find **FactFinancialTable** and **Dim Tables**
2. Check the box to **add them to the model**  
3. Click **Create**  
4. Click **Open the Data model** 

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/4edcdee863d34f09bca213b50684ef61998f4447/03-Fraud%20Analysis/Reference%20Pictures/%7BAC6C6FBC-989A-44EC-9FA9-5C1068E674DF%7D.png)

5. Enter **Editing Mode**

Ensure the Columns with **Whole Numbers** and **Decimal Numbers** are Summarized by **None**

**Tables : NumberOfDependents, Zip, ApprovedAmount_Dollar, CreditScore, RequestedAmount_Dollar, Return_Percentage, Value_Dollar and YearsOfBeingCustomer**

![alt text]({811802D3-1B2D-4D09-AFFA-B16E25384C96}.png)

Create One to One relationships between your Factual and Dim Tables

![alt text]({774CDA62-1850-4584-9028-787DA2025787}.png)

---

## 🚀 Step 5: Generate a blank Power BI Report to Discover your Data!  

💡 **Why?** Power BI can now connect directly to your **semantic model**.  

### 1️⃣ Click the ***Create New Power BI option**

![alt text]({FC9D1153-380A-4BD2-BAF6-0CEA6B30235F}.png)

### Build a report to discover Low Risk Investments with High Returns (More than 10%)

## 1. Open Your Dataset and Start a New Report

1. Go to your **Fabric Workspace**.  
2. Find the **Dataset** (semantic model) for your financial data.  
3. Click **Create report** (or “New report”) from that dataset.  
4. You’ll see a **blank canvas** with the **Data** pane on the right (listing your tables/fields).

---

## 2. Filter to Only Investment Documents

1. On the **right** side, in the **Data** pane, expand your **FactFinancialTable** (or whichever name you used).  
2. Locate the **DocumentType** field.  
3. **Drag** `DocumentType` into the **Filters** pane (on the right).  
   - Under “Filters on this page” (or “Filters on all pages”), choose **Basic filtering**.  
4. Select **"Investment"** to include only rows with `DocumentType = "Investment"`.  
5. Now all visuals on this page will only show investment rows.

---

## 3. Create a Table Visual

1. In the **Visualizations** pane (right side), click the **Table** icon (the small grid).  
2. A **blank Table** visual appears on the canvas.  
3. **Select** that Table visual so it’s highlighted.

---

## 4. Add Fields to the Table

1. In the **Data** pane, expand **FactFinancialTable** (or your table name).  
2. **Drag** these fields into the **Values** area of the Table visual:
   - `ClientID` (or `ClientName`, if you have it)  
   - `InvestmentType`  
   - `Risk` (text field: "Low", "Medium", "High")  
   - `Return_Percentage` (numeric)  
3. You’ll see each row of data in the table with those columns.

---

## 5. Filter for "Low" Risk

Since `Risk` is **text**, you’ll filter by **exact value** instead of numeric comparison:

1. Still in the **Filters** pane, under “Filters on this visual,” **drag** `Risk` from the Data pane.  
2. Change to **Basic filtering** (if not already).  
3. **Check** the box for **"Low"** only.  
4. Now the table displays only rows where `Risk = "Low"`.

---

## 6. Filter for Return_Percentage > 10

1. Also **drag** `Return_Percentage` into **Filters on this visual**.  
2. Since `Return_Percentage` is numeric, you’ll see options like “is greater than,” “is less than,” etc.  
3. Choose **“is greater than 10”**.  
   - If you store 10 as 10.0, it means 10%. If you store 0.10 for 10%, then filter “> 0.10.”

---

## 7. Check the Table Results

- Your table now shows **only** investments with **Risk = "Low"** and **Return_Percentage > 10**.  
- This effectively highlights **low-risk, high-return** rows—potentially suspicious or extremely profitable.

---

## 8. (Optional) Add a Slicer for Client Attributes

1. If you have a **DimClient** table with fields like `ClientStatus` or `YearsAsCustomer`, you can add a slicer:  
   - Insert a **Slicer** visual (the funnel icon).  
   - Drag `ClientStatus` onto it.  
   - Now you can filter the table further by "Platinum" or "Gold" clients, for instance.

---

## 9. Format and Save the Report

1. Click the **Table** visual → go to the **Format** (paint roller) in the Visualizations pane.  
2. Adjust styles, headers, or conditional formatting if you like.  
3. **Rename** this page (bottom tab) to **"Low-Risk High-Return Investments"**.  
4. Click **Save** (top-right).  
   - Name your report.  
   - It’s now saved to your Fabric workspace.

---

## Conclusion

With these steps, you’ve built a **Power BI** report in **Fabric** that focuses on **investments** where **Risk** is “Low” and **Return_Percentage** exceeds 10. This helps detect anomalies or potential fraud in your financial dataset.

---

## 🚀 Step 6: Share & Refresh the Power BI Report  

💡 **Best Practices**:  

- **Share the Report**: Click **Share** → Add colleagues via email  
- **Schedule Data Refresh**:  
  - In **Power BI** → Click **Dataset Settings**  
  - Enable **Direct Query Mode** for **real-time updates**  

✅ **Outcome**: Your **Power BI report** is **live, shareable, and always up-to-date** with new financial data!  

---

# 🎯 Summary of Key Steps  

### **🔹 Step 1: Store JSON files in Fabric Lakehouse**  
- Upload your **financial JSON data** into **Files/json** in Fabric  

### **🔹 Step 2: Run PySpark Notebook to Create a Table**  
- **Transform raw JSON into a structured table** (`InvestmentPortfolio`)  

### **🔹 Step 3: Create a Semantic Model**  
- **Connect Fabric data to Power BI** using **Direct Lake**  

### **🔹 Step 4: Generate Power BI Report**  
- **Auto-generate a financial dashboard** in Power BI  

### **🔹 Step 5: Share & Refresh the Report**  
- **Share with stakeholders & enable real-time updates**  

---
