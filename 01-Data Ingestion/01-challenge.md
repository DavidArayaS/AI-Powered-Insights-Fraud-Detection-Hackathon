# 🏆 Challenge 1: Setting Up Fabric & Storage Solutions.

## 📖 Scenario  
Contoso, a global company, is implementing a **cloud-based AI-powered fraud detection system**. They need a **scalable and secure solution** to store and process financial transaction PDFs before analysis.  

Your task is to **set up Microsoft Fabric and Data Storage Solutions** to build the foundation for this system.  

---

## 🎯 Your Mission  
By completing this challenge, you will:  

✅ Set up **Microsoft Fabric Capacity**  
✅ Create a **OneLake Lakehouse** to store financial transaction PDFs  
✅ Upload the provided PDFs to **OneLake**  
✅ Create & Configure a **Service Principal** for authentication  
✅ Assign appropriate **permissions** in Fabric & Azure Storage  

> **Note:** You will not process the documents yet—this is about **building the data pipeline** to store and prepare them.  

---

## 🚀 Step 1: Create Microsoft Fabric Capacity  
💡 **Why?** Microsoft Fabric provides the necessary **capacity to store and process large datasets**.  

### 1️⃣ Create Fabric Capacity in Azure  
🔹 Using the **Azure Portal**, create a **Fabric Capacity** resource that will support the **Lakehouse** and data pipeline.  

🔹 **What settings should you configure?**  
   - Which **SKU** is required for this challenge?  
   - What **security features** should you enable?  

✅ **Best Practice**: Consider setting up **RBAC (Role-Based Access Control)** to manage access.  

---

## 🚀 Step 2: Assign Fabric Capacity in Microsoft Fabric  
💡 **Why?** The Fabric workspace must be **assigned to a capacity** before you can use it.  

### 1️⃣ Assign Fabric Capacity  
🔹 Navigate to **Microsoft Fabric** and assign the newly created **Fabric Capacity** to a workspace.  

🔹 **Where in the Fabric UI can you manage capacity assignments?**  

✅ **Outcome**: Your **Fabric workspace** should now be connected to a **Fabric Capacity**.  

---

## 🚀 Step 3: Create a OneLake Lakehouse  
💡 **Why?** A **OneLake Lakehouse** is needed to store **unprocessed PDFs** before AI processing.  

### 1️⃣ Create a Fabric Lakehouse  
🔹 In **Microsoft Fabric**, create a **new Lakehouse** inside your workspace.  

🔹 **What folder structure would be best for organizing financial PDFs?**  

✅ **Best Practice**: Keep a **structured folder hierarchy** for organized data.  

---

## 🚀 Step 4: Upload the PDFs to OneLake  
💡 **Why?** The AI models need **structured and accessible financial documents**.  

### 1️⃣ Upload PDF Files  
🔹 Upload the provided **financial transaction PDFs** to **OneLake**.  

🔹 **Where should you upload the files inside the Lakehouse?**  

✅ **Best Practice**: Use the Data provided by your instructor.  


---

## 🚀 Step 5: Create a Storage Account  
💡 **Why?** This **Storage Account** will be used for **future data transfers from Fabric**.  

### 1️⃣ Create an Azure Storage Account  
🔹 Using the **Azure Portal**, create a **Storage Account**.  

🔹 **What configuration settings are important for security and performance?**  

✅ **Outcome**: Your **Storage Account** is now ready for future **data movement**.  

---

## 🚀 Step 6: Create & Configure a Service Principal  
💡 **Why?** Azure services require **authentication** to **access and transfer data securely**.  

### 1️⃣ Create a Service Principal in Azure Entra ID  
🔹 In **Azure Entra ID (Active Directory)**, register a **new application** for the **Service Principal**.  

🔹 **What two key pieces of information do you need after creating the Service Principal?**  

✅ **Outcome**: Your **Service Principal** is registered, but it still needs **permissions**.  

---

## 🚀 Step 7: Generate & Store Service Principal Credentials  
💡 **Why?** The **Service Principal** needs **credentials** to authenticate.  

### 1️⃣ Create a Client Secret  
🔹 Generate a **Client Secret** and **securely store** its value.  

🔹 **Why is it important to save the secret value immediately?**  

✅ **Outcome**: You now have the **Client ID, Tenant ID, and Secret Key** for authentication.  

---

## 🚀 Step 8: Assign Permissions in Fabric & Blob Storage  
💡 **Why?** The **Service Principal** must be granted **access** to Fabric and Azure Storage.  

### 1️⃣ Enable Service Principal Authentication in Fabric  
🔹 In **Microsoft Fabric**, enable **Service Principal authentication** for **Fabric APIs**.  

🔹 **What Fabric Admin Setting must be changed to allow API access?**  

✅ **Outcome**: The **Service Principal** can now **authenticate with Fabric APIs**.  

### 2️⃣ Assign Permissions in Storage Account  
🔹 Go to the **Storage Account** → **Access Control (IAM)**  

🔹 Assign the following **roles** to the **Service Principal**:  
   ✅ **Storage Blob Data Contributor**  
   ✅ **Storage Account Contributor**  
   ✅ **Cognitive Services Contributor** (*For Document Intelligence*)  

🔹 **Why are these permissions necessary for the next steps of the challenge?**  

✅ **Outcome**: The **Service Principal now has full access** to **Fabric & Blob Storage**.  

---

## 🚀 Step 9: Create a Document Intelligence Service in Azure  
💡 **Why?** The **Service** will analyze the **raw data**.  

---

## 🚀 Step 10: Create an Standard LRS Storage Account
💡 **Why?** The **Service** store you **analyzed JSON data**.  

---

## 🏁 Final Challenge Checkpoints  
✅ Can you verify that **Fabric Capacity** is assigned correctly?  
✅ Do all **financial PDFs** appear in **OneLake**?  
✅ Does your **Two Storage Accounts, and Document Intelligence service** exist and are ready for use?  
✅ Is your **Service Principal configured** and has necessary **permissions**?  

Once all steps are completed, you are ready to move on to **Challenge 2! 🚀**  

---

## ❓ Troubleshooting Tips  
🔹 If **Fabric** does not recognize your **Service Principal**, check if **API access** is enabled.  
🔹 If you cannot **upload files to OneLake**, verify the assigned **capacity and workspace settings**.  
🔹 If the **Storage Account** is not accessible, ensure the correct **RBAC roles** are assigned