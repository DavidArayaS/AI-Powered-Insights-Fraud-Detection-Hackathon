# 📖 Solution to Challenge 5: Creating a Power BI Report from Financial Data in Microsoft Fabric  

---

## 🔹 Objective  
This guide will walk you through the entire process of extracting, transforming, and visualizing financial data using **Microsoft Fabric, Lakehouse, and Power BI**.

✅ Store and process financial data in **Fabric Lakehouse**  
✅ Run a **Notebook (PySpark) to transform data**  
✅ Create a **Semantic Model**  
✅ Generate a **Power BI reports**  

---

## 🚀 Step 1: Ensure Your Data is in Fabric Lakehouse  

💡 **Before proceeding, make sure** that your **financial data (JSON files)** are already uploaded to Fabric Lakehouse under `Files/`.  

### 1️⃣ Verify Data Storage in Fabric Lakehouse  
1. Open **Microsoft Fabric**  
2. Navigate to your **Lakehouse**  
3. Under the **Files** section, confirm the presence of `yourfolder` folder  
4. Ensure it contains **analyzed JSON files**  

✅ **Outcome**: Your JSON files are now stored in Fabric Lakehouse.  

---

## 🚀 Step 2: Run the PySpark Notebook to Transform Data  

💡 **Why?** The raw JSON data must be structured into a **relational format** before it can be used in Power BI.  

### 1️⃣ Open a Fabric Notebook  

1. In **Fabric**, go to your **Lakehouse**  
2. Click **+ New** → **Notebook**  
3. Select **PySpark** as the language  

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/b5cf26084f2a7df335ce0c432371cfbfa0421abb/03-Fraud%20Analysis/Reference%20Pictures/%7BE2B88327-CADC-406A-91D1-7B83CB545751%7D.png)

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/f7f822f447deaa803341b3c3d3ebabf6ff02f0cf/03-Fraud%20Analysis/Reference%20Pictures/%7B1333AEA5-3BA2-4D7E-A87E-46ECCFDD3797%7D.png)

### 2️⃣ Copy & Paste the PySpark Code 

[FactFinancialTable.py](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/c3af96e9085107104005d86344f07a6f4a7c6e7b/03-Fraud%20Analysis/FactFinancialTable.py)

### 3️⃣ Run the Notebook  
- Click **Run All** to execute the script  
- Wait for the process to complete  

✅ **Outcome**: A new table **FactFinancialTable** is now available in your **Fabric Lakehouse**.  



---
## 🚀 Step 3: Create the Lookup or Dimension Tables

1. Use the Excel files provided with your [Dimension Tables](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/9868ec5cf1f4315ae16421983092e1909d0662e0/Data%20Sources/Dimension%20Tables.zip)

2. Open your Lakehose
3. Click **Get data**
4. Select **New Dataflow Gen2**
5. Select the **Enter Data** Option
6. Create a table for each of the Excel files using their content

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/f7f822f447deaa803341b3c3d3ebabf6ff02f0cf/03-Fraud%20Analysis/Reference%20Pictures/%7B26DF6A17-F66B-492C-BEE5-07A7769F0101%7D.png)

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/73581913b9b0deb877f6802519195eb50ee19283/03-Fraud%20Analysis/Reference%20Pictures/%7BBC3303EC-5A33-4CB0-9BBC-BE9836A7DD67%7D.png)

7. **Publish** the tables, they should now be under Tables/ in your Lakehouse

---

## 🚀 Step 4: Create a Semantic Model  

💡 **Why?** The semantic model allows **Power BI** to interact with your **Fabric data**.  

### 1️⃣ Create a New Semantic Model  
1. Go to **Microsoft Fabric**  
2. Click open your Lakehouse and **Click → **Semantic Model**  
3. Name it **Financial-Semantic-Model**  

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/b5cf26084f2a7df335ce0c432371cfbfa0421abb/03-Fraud%20Analysis/Reference%20Pictures/%7B73E204B3-284D-4D78-B3A3-BDCAF807DC68%7D.png)


### 2️⃣ Select Your Financial Tables
1. In the **Select tables** section, find **FactFinancialTable** and **Dim Tables**
2. Check the box to **add them to the model**  
3. Click **Create**  
4. Click **Open the Data model** 

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/f28402554e0ed6ac1e8b909437ebb55451bec134/03-Fraud%20Analysis/Reference%20Pictures/%7BDD1083C8-3569-4E0E-A7DA-700978A6854E%7D.png)

5. Enter **Editing Mode**

Ensure the Columns with **Whole Numbers** and **Decimal Numbers** are Summarized by **None**

**Tables : NumberOfDependents, Zip, ApprovedAmount_Dollar, CreditScore, RequestedAmount_Dollar, Return_Percentage, Value_Dollar and YearsOfBeingCustomer**

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/d9955813ef99659c31613a5cd7d2239db597d6a4/03-Fraud%20Analysis/Reference%20Pictures/%7B811802D3-1B2D-4D09-AFFA-B16E25384C96%7D.png)

Create One to One relationships between your Factual and Dim Tables

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/d9955813ef99659c31613a5cd7d2239db597d6a4/03-Fraud%20Analysis/Reference%20Pictures/%7B774CDA62-1850-4584-9028-787DA2025787%7D%20(1).png)

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/4edcdee863d34f09bca213b50684ef61998f4447/03-Fraud%20Analysis/Reference%20Pictures/%7BAC6C6FBC-989A-44EC-9FA9-5C1068E674DF%7D.png)
---

## 🚀 Step 5: Generate a blank Power BI Report to Discover your Data!  

💡 **Why?** Power BI can now connect directly to your **semantic model**.  

### 1️⃣ Click the ***Create New Power BI option to Build any of the following reports**

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/d9955813ef99659c31613a5cd7d2239db597d6a4/03-Fraud%20Analysis/Reference%20Pictures/%7BFC9D1153-380A-4BD2-BAF6-0CEA6B30235F%7D.png)

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
### Building a “Suspicious Loan Approvals” Report in Power BI 

Below is a **step-by-step** guide to create a Power BI report in **Microsoft Fabric** that highlights **Loan** documents where:

- **ApprovedAmount_Dollar** > 30,000  
- **CreditScore** < 650  
- **ProofOfIdentityProvided** = "No"  
- **YearsAsCustomer** < 5  

This scenario suggests a suspicious approval for applicants with low credit, short relationship history, and no identity proof.

---

## 1. Open Your Dataset and Start a New Report

1. Go to your **Fabric Workspace**.  
2. Locate the **Dataset** (semantic model) containing your **FactFinancialTable** and dimensions.  
3. Click **Create report** (or “New report”) from that dataset.  
4. You’ll see a **blank canvas** with the **Data** pane on the right (listing your tables/fields).

---

## 2. Create a Page Filter for Loans Only

1. On the **right** side, in the **Data** pane, expand your **FactFinancialTable**.  
2. Locate **DocumentType**.  
3. **Drag** `DocumentType` into the **Filters** pane (on the right).  
   - Under “Filters on this page” (or “Filters on all pages”), choose **Basic filtering**.  
4. Select **"Loan"** to include only rows with `DocumentType = "Loan"`.  
5. Now all visuals on this page will only show **loan** documents.

---

## 3. Create a Table Visual

1. In the **Visualizations** pane (right side), click the **Table** icon (the small grid).  
2. A **blank Table** visual appears on the canvas.  
3. **Select** that Table visual so it’s highlighted.

---

## 4. Add Fields to the Table

1. In the **Data** pane, expand **FactFinancialTable** (or your table name).  
2. **Drag** the following fields into the **Values** area of the Table visual:
   - `ApplicantID` (or `ApplicantName`)  
   - `CreditScore`  
   - `ApprovedAmount_Dollar`  
   - `ProofOfIdentityProvided`  
   - `YearsAsCustomer` (if it’s in **DimClient** or **DimApplicant**, you can still drag it in if relationships are set up)  

3. The table now shows each **Loan** row with these columns.

---

## 5. Apply Numeric Filters

### 5.1 Filter “ApprovedAmount_Dollar > 30000”

1. In the **Filters** pane, under “Filters on this visual,” **drag** `ApprovedAmount_Dollar` from the Data pane.  
2. Select **Advanced filtering** (or numeric).  
3. Set **“is greater than” 30000**.  
4. Click **Apply** or confirm.

### 5.2 Filter “CreditScore < 650”

1. Also **drag** `CreditScore` into **Filters on this visual**.  
2. Select **Advanced filtering**.  
3. Set **“is less than” 650**.  
4. Click **Apply**.

---

## 6. Apply Categorical Filters

### 6.1 ProofOfIdentityProvided = “No”

1. Still in **Filters on this visual**, **drag** `ProofOfIdentityProvided` from the Data pane.  
2. Change to **Basic filtering** (if it’s text).  
3. Check the box for **“No”**.  
4. The table now only shows rows where identity proof is missing.

### 6.2 YearsAsCustomer < 5

1. **Drag** `YearsAsCustomer` into **Filters on this visual**.  
2. If it’s numeric, select **Advanced filtering** → “is less than” 5.  
3. Click **Apply**.

---

## 7. Review the Table Results

- Your table now shows **only** loan rows where:
  1. **ApprovedAmount_Dollar** > 30,000  
  2. **CreditScore** < 650  
  3. **ProofOfIdentityProvided** = “No”  
  4. **YearsAsCustomer** < 5  

- This combination is highly suspicious: big loans, low credit, short history, and no identity proof.

---

## 8. (Optional) Add Extra Slicers

1. If you want to slice by **DimApplicant** attributes (e.g., `EmployedWith`) or **DimClient** (`ClientStatus`), insert a **Slicer** visual.  
2. Drag the attribute into the slicer to refine your results further.

---

## 9. Format and Save the Report

1. Click the **Table** visual → open the **Format** (paint roller) in the Visualizations pane to style it.  
2. Rename this page (bottom tab) to **“Suspicious Loan Approvals”** (or similar).  
3. Click **Save** (top-right). Name the report.  
4. It’s now saved to your Fabric workspace for future analysis or sharing.

---

## Conclusion

With these steps, you’ve built a **Power BI** report that spotlights **loans** matching critical fraud indicators:

- **High** Approved Amount  
- **Low** Credit Score  
- **No** Identity Proof  
- **Short** Customer Relationship

This helps you quickly identify red flags in your fictional dataset. 
---

### Build a report to discover Suspicious Partially Approved Loans with Missing Data and Low Credit Scores

## 1. Open Your Dataset and Start a New Report

1. Go to your **Fabric Workspace**.  
2. Locate your **Dataset** (semantic model) with financial data.  
3. Click **Create report** (or “New report”) from that dataset.  
4. You’ll see a **blank canvas** with the **Data** pane on the right (listing your tables/fields).

---

## 2. Filter to Only Loan Documents

1. On the **right side**, in the **Data** pane, expand your **FactFinancialTable**.  
2. Locate the **DocumentType** field.  
3. **Drag** `DocumentType` into the **Filters** pane (on the right).  
   - Choose **Basic filtering**.  
4. Select **"Loan"** to include only rows with `DocumentType = "Loan"`.  
5. Now, all visuals on this page will only show loan documents.

---

## 3. Create a Table Visual

1. In the **Visualizations** pane (right side), click the **Table** icon (the small grid).  
2. A **blank Table** visual appears on the canvas.  
3. **Select** that Table visual so it’s highlighted.

---

## 4. Add Fields to the Table

1. In the **Data** pane, expand your tables, and drag these fields into the **Values** area of the Table visual:
   - `ApplicantID`
   - `ApplicantName`
   - `ProofOfIdentityProvided`
   - `ApprovalStatus`
   - `CreditScore`
   - `Street` *(from DimAddress)*
   - `State` *(from DimAddress)*
   - `City` *(optional)*

2. The table now displays each loan document with these columns.

---

## 4. Filter for "Partially Approved" Loans

1. In the **Filters** pane under “Filters on this visual,” **drag** `ApprovalStatus`.
2. Choose **Basic filtering**.
3. Select **"Partially Approved"**.
4. Now the table displays only partially approved loans.

---

## 5. Filter for Very Low Credit Scores (below 500)

1. Drag `CreditScore` into **Filters on this visual**.
2. Select **Advanced filtering**.
3. Set filter to **“is less than” 500**.
4. Click **Apply**.

---

## 6. Filter for Missing Proof of Identity

1. Drag `ProofOfIdentityProvided` into **Filters on this visual**.
2. Set to **Basic filtering**.
3. Select **"No"** only.
4. This filters for loans without identity proof.

---

## 6. Filter for Missing Address Information

1. Drag `Street` into **Filters on this visual**:
   - Select **Advanced filtering → "is blank"**.
2. Drag `State` into **Filters on this visual**:
   - Select **Advanced filtering → "is blank"**.
3. Use the logical **"Or"** operator between these conditions.
4. Now, the table highlights entries missing critical address details.

---

## 7. Review the Results

Your table now displays **only suspicious loan records** characterized by:

- **Partial Approval**
- **CreditScore below 500**
- **No Proof of Identity**
- **Incomplete address information (Street or State missing)**

---

## 7. (Optional) Additional Slicers

- Add slicers (e.g., from **DimApplicant** or **DimClient**) to further drill into the suspicious loans by applicant employment status or customer type.

---

## 8. Format and Save the Report

1. Click your **Table** visual → go to the **Format** (paint roller) pane.
2. Adjust visuals for clarity and readability.
3. Rename this report page to **"Suspicious Partially Approved Loans"**.
4. Click **Save** (top-right), name your report clearly, and store it in your Fabric workspace.

---

***Get deeper insights of your data with Copilot!***

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/9678e1307b0fb93ce45e1e4ad79e1de8cba42b40/03-Fraud%20Analysis/Reference%20Pictures/%7B8ED545F2-F0ED-473C-BD10-DD6A6FA4A855%7D.png)

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/5647d69aef706b409068bace5cc88b58310f1a39/03-Fraud%20Analysis/Reference%20Pictures/%7B48D6AC86-184B-4356-B7A1-6EE4B814C34C%7D.png)

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/5647d69aef706b409068bace5cc88b58310f1a39/03-Fraud%20Analysis/Reference%20Pictures/%7BD15A33FC-D6FB-4849-ACD7-B8169D3D93BE%7D.png)


---

## Conclusion

With these steps, you've created a targeted **Power BI** report in **Fabric** that identifies potentially fraudulent or suspicious loan approvals based on critical red flags.


---
### What other reports can you imagine building?

Lacking ideas? Ask Copilot!

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/72b9f51980e95ad59848faa982257b236cdd22b7/03-Fraud%20Analysis/Reference%20Pictures/%7BE2C915BA-A08A-47D5-AD4A-CE2876CAF8CB%7D.png)



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
