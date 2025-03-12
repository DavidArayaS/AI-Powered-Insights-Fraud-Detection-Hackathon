# 🏆 Challenge 1: Setting Up Fabric & Storage Solutions  

## 📖 Scenario  
You need to implement a **cloud-based solution** for securely storing and managing financial transaction PDFs. This challenge focuses on **building the foundation** for data storage and access using **Microsoft Fabric and Azure Storage**.  

Your goal is to set up the **necessary infrastructure** to support a scalable data pipeline.  

> **Note:** If you **already completed the Fabric Capacity setup** and **Service Principal creation** as per the **prerequisites email**, you can **skip those steps** and proceed with the rest of the challenge.  

---

## 🎯 Your Mission  
By completing this challenge, you will:  

✅ Set up **Microsoft Fabric Capacity** *(skip if completed in prerequisites)*  
✅ Create a **OneLake Lakehouse** to store financial transaction PDFs  
✅ Download, unzip, and upload **financial data** to **OneLake**  
✅ Create & Configure a **Service Principal** for authentication *(skip if completed in prerequisites)*  
✅ Assign appropriate **permissions** in Fabric & Azure Storage  
✅ Retrieve **Document Intelligence API endpoint & keys** for later use  

> **Reminder:** This challenge is about **building the data pipeline**. You will not process the documents yet.  

---

## 🚀 Step 1: Create Microsoft Fabric Capacity *(Skip if completed in prerequisites)*  
💡 **Why?** Microsoft Fabric provides the necessary **capacity to store and process large datasets**.  

### 1️⃣ Create Fabric Capacity in Azure  
🔹 Use the **Azure Portal** to create a **Fabric Capacity** resource.  

🔹 **Things to consider:**  
   - What **SKU** is required for this challenge?  
   - Should **security features** like Private Link be enabled?  

✅ **Best Practice**: Configure **RBAC (Role-Based Access Control)** to manage access.  

---

## 🚀 Step 2: Assign Fabric Capacity in Microsoft Fabric *(Skip if completed in prerequisites)*  
💡 **Why?** The Fabric workspace must be **assigned to a capacity** before you can use it.  

### 1️⃣ Assign Fabric Capacity  
🔹 In **Microsoft Fabric**, assign the **Fabric Capacity** to your workspace.  

🔹 **Hint:** Where in the Fabric UI can you manage capacity assignments?  

✅ **Outcome**: Your **Fabric workspace** should now be connected to a **Fabric Capacity**.  

---

## 🚀 Step 3: Create a OneLake Lakehouse  
💡 **Why?** A **OneLake Lakehouse** is needed to store **unprocessed PDFs** before AI processing.  

### 1️⃣ Create a Fabric Lakehouse  
🔹 In **Microsoft Fabric**, create a **new Lakehouse** inside your workspace.  

🔹 **Hint:** What folder structure would be best for organizing financial PDFs?  

✅ **Best Practice**: Keep a **structured folder hierarchy** for better organization.  

---

## 🚀 Step 4: Download & Upload Financial Data to OneLake  
💡 **Why?** Your **AI models** need structured **financial PDFs** to analyze.  

### 1️⃣ Download and Extract the Financial Data  
🔹 Download the **financial data ZIP file** from the following link:  
   🔗 [Financial Data.zip](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/05f385b28e7d4215b0e1bf52eeaabf63b70e7c1a/Data%20Sources/Financial%20Data.zip)  

🔹 Extract the **ZIP file** on your local machine.  
🔹 Locate the extracted **Financial Data** folder containing the transaction PDFs.  

### 2️⃣ Upload Financial Data to OneLake  
🔹 Open **Microsoft Fabric** → Navigate to **YourLakehouse**.  
🔹 Click on **Files** (inside the Lakehouse).  
🔹 Click **Upload Folder** → Select the extracted Folder with the **PDF files**.  

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/f6b939b949003bbd1655cd718a81b2852f2d4c51/01-Data%20Ingestion/Reference%20Pictures/%7BB587EEAC-7F75-4991-9FCF-98F72CEF18CF%7D.png)

✅ **Outcome**: Your **financial data** is now **organized and available** in OneLake.  

---

## 🚀 Step 5: Create a Storage Account  
💡 **Why?** This **Storage Account** will be used for **future data transfers from Fabric**.  

### 1️⃣ Create an Azure Storage Account  
🔹 Use the **Azure Portal** to create a **Storage Account**.  

🔹 **Things to consider:**  
   - What replication type is best for performance and security?  

✅ **Outcome**: Your **Storage Account** is now ready for future **data movement**.  

---

## 🚀 Step 6: Create & Configure a Service Principal *(Skip if completed in prerequisites)*  
💡 **Why?** A **Service Principal** allows secure, automated authentication between services.  

### 1️⃣ Create a Service Principal in Azure Entra ID  
🔹 In **Azure Entra ID (Active Directory)**, register a **new application** for the **Service Principal**.  

✅ **Outcome**: Your **Service Principal** is registered but still needs **permissions**.  

---

## 🚀 Step 7: Generate & Store Service Principal Credentials *(Skip if completed in prerequisites)*  
💡 **Why?** The **Service Principal** needs **credentials** to authenticate.  

### 1️⃣ Create a Client Secret  
🔹 Generate a **Client Secret** and **securely store** its value.  

✅ **Outcome**: You now have the **Client ID, Tenant ID, and Secret Key** for authentication.  

---

## 🚀 Step 8: Assign Permissions in Fabric & Blob Storage  
💡 **Why?** The **Service Principal** must be granted **access** to Fabric and Azure Storage.  

✅ **Outcome**: The **Service Principal now has full access** to **Fabric & Blob Storage**.  

---

## 🚀 Step 9: Create & Retrieve Document Intelligence Service Endpoint & Keys  
💡 **Why?** The **Document Intelligence API** will be used later to process financial PDFs.  

🔹 **Steps to retrieve the API endpoint and keys**:  
   1. Go to **Azure Portal** → Search for **Document Intelligence**.  
   2. Select your **Document Intelligence instance**.  
   3. Click on **Keys and Endpoint** in the left menu.  
   4. **Copy & Save** the following:  
      - **Endpoint URL**  
      - **Primary Key**  

✅ **Outcome**: You now have **authentication details** to use **Document Intelligence API** later.  

---

## 🚀 Step 10: Create a Standard LRS Storage Account  
💡 **Why?** This **Storage Account** will be used to store **analyzed JSON data**.  


✅ **Outcome**: The **Storage Account** is ready for storing processed data.  

[Supporting Document](https://learn.microsoft.com/en-us/fabric/onelake/onelake-azure-storage-explorer)

---

## 🏁 Final Challenge Checkpoints  
✅ Is **Fabric Capacity** assigned correctly? *(Skip if already done in prerequisites)*  
✅ Do all **financial PDFs** appear in **OneLake** under **/Files/FinancialData/**?  
✅ Do both **Storage Accounts** and the **Document Intelligence Service** exist and are they ready for use?  
✅ Is your **Service Principal configured** with the necessary **permissions**?

Once all steps are completed, you are ready to move on to **Challenge 2! 🚀**  

---

## ❓ Troubleshooting Tips  
🔹 If **Fabric** does not recognize your **Service Principal**, check if **API access** is enabled.  
🔹 If you cannot **upload files to OneLake**, verify the assigned **capacity and workspace settings**.  
🔹 If the **Storage Account** is not accessible, ensure the correct **RBAC roles** are assigned.  
🔹 If the **Document Intelligence API** is not working, verify the **endpoint and keys** are correct.  
