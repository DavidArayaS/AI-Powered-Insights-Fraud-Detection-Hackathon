# 🏆 Challenge 5: Building a Power BI Report from Financial Data in Microsoft Fabric  

## 📖 Scenario  
Contoso, a global financial firm, is looking to **automate the analysis of investment portfolios**. They have **unstructured JSON data** stored in **Microsoft Fabric Lakehouse** and want to transform this into a **Power BI report** that provides real-time insights.  

Your task is to **process, structure, and visualize financial data** using Fabric and Power BI.  

---

## 🎯 Your Mission  
By completing this challenge, you will:  

✅ Process **JSON investment data** from **Fabric Lakehouse**  
✅ Use **PySpark in a Fabric Notebook** to structure the data  
✅ Create a **Semantic Model** for Power BI integration  
✅ Automatically generate a **Power BI report**  
✅ Ensure the report is **shareable and refreshable**  

> **Note:** The goal is to **connect data from Fabric to Power BI** while ensuring **automated updates** and **real-time insights**.  

---

## 🚀 Step 1: Ensure Your Data is Stored in Fabric Lakehouse  
💡 **Why?** Power BI relies on **structured data** stored in **Fabric Lakehouse**.  

### 1️⃣ Verify Data Storage  
🔹 Open **Fabric Lakehouse** and confirm that your **financial data** is available in `Files/json`.  

🔹 **How can you check that the JSON data is properly structured?**  

✅ **Outcome**: Your **financial data** is accessible in Fabric Lakehouse.  

---

## 🚀 Step 2: Transform JSON Data Using a Fabric Notebook  
💡 **Why?** The raw **unstructured JSON data** must be **transformed into a table** before Power BI can use it.  

### 1️⃣ Use a Fabric Notebook to Process Data  
🔹 Open a new **PySpark Notebook** in Fabric.  

🔹 **What transformations are needed to extract meaningful financial insights?**  

✅ **Outcome**: A **structured Delta table** is created in Fabric Lakehouse.  

---
## 🚀 Step 3: Create the Lookup or Dimension Tables

1. Use the Excel files provided with your PDF datasource
---

---

## 🚀 Step 4: Create a Semantic Model  
💡 **Why?** A **Semantic Model** allows Power BI to efficiently **query and analyze** Fabric data.  

### 1️⃣ Connect Fabric Data to Power BI  
🔹 Create a **Direct Lake Semantic Model** in Fabric.  

🔹 **Which table should be used for the model, and why?**  

✅ **Outcome**: Power BI can now **connect directly to Fabric Lakehouse**.  

---

## 🚀 Step 5: Generate a Power BI Report  
💡 **Why?** Power BI **automatically detects data** from the **Semantic Model** and generates **visual insights**.  

### 1️⃣ Explore the Data in Power BI  
🔹 Open **Power BI** and select **Explore with Power BI**.  

🔹 **What insights can be visualized from the financial data?**  

✅ **Outcome**: A **default dashboard** is generated in Power BI.  

---

## 🚀 Step 6: Share & Refresh the Power BI Report  
💡 **Why?** A **real-time dashboard** ensures that stakeholders always see **updated financial data**.  

### 1️⃣ Enable Sharing & Automatic Refresh  
🔹 Share the report with **team members**.  

🔹 **How can you ensure the Power BI report remains up-to-date?**  

✅ **Outcome**: Your **financial report** is **live, refreshable, and shareable**.  

---

## 🏁 Final Challenge Checkpoints  
✅ Is your **financial data accessible** in Fabric Lakehouse?  
✅ Have you **transformed raw JSON data** into a **structured table**?  
✅ Does **Power BI successfully connect** to your Semantic Model?  
✅ Is the **Power BI report interactive, insightful, and shareable**?  

Once all steps are completed, you have **successfully built a real-time financial dashboard! 🚀**  

---

## ❓ Troubleshooting Tips  
🔹 If **Power BI does not show data**, check that the **Semantic Model includes the correct table**.  
🔹 If the **report does not update**, verify that **Direct Query Mode** is enabled.  
🔹 If the **Notebook fails**, confirm the **JSON file format** and **data transformations**.  
