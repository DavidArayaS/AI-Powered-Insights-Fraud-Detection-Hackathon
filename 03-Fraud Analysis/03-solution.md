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

[FactFinancialTable.py](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/c3af96e9085107104005d86344f07a6f4a7c6e7b/03-Fraud%20Analysis/FactFinancialTable.py)

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
![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/73581913b9b0deb877f6802519195eb50ee19283/03-Fraud%20Analysis/Reference%20Pictures/%7BBC3303EC-5A33-4CB0-9BBC-BE9836A7DD67%7D.png)

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

### 1️⃣ Click the ***Create New Power BI option**

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
