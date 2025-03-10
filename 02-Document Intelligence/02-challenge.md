# 🏆 Challenge 2: Automating Document Processing with Logic Apps  

## 📖 Scenario  

Contoso needs an automated pipeline to process financial PDFs using **Azure AI services**. The goal is to extract structured financial data and save the results in an**Azure Storage Account** for further analysis.  

Your task is to build an **end-to-end AI-powered document processing pipeline** using **Azure Logic Apps, Azure Data Factory (ADF), and Azure Document Intelligence**.  

---

## 🎯 Your Mission  

By completing this challenge, you will:  

✅ Set up an **Azure Logic App** to trigger PDF processing automatically  
✅ Enable **Managed Identity** for secure access to resources  
✅ Assign **permissions** to the Logic App for storage and AI processing  
✅ Use **Document Intelligence (Form Recognizer)** to analyze PDFs  
✅ Create an **ADF pipeline** to move PDFs from **Fabric** to a **Storage Account**  
✅ Store analyzed **JSON outputs** in **Storage Account**  
✅ Verify **processed files** are saved in **Storage Account**  

---

## 🚀 Step 1: Create a Logic App  

💡 **Why?** The Logic App will **automate** the process of detecting new PDFs and triggering **Document Intelligence** analysis.  

### 1️⃣ Create an Azure Logic App  
🔹 Using **Azure Portal**, create a new **Logic App (Consumption Plan)**.  

🔹 **What settings should you configure during creation?**  

✅ **Outcome**: A Logic App is created and ready for configuration.  

---

## 🚀 Step 2: Enable Managed Identity for the Logic App  

💡 **Why?** The Logic App needs authentication to interact with **Azure Storage** and **Document Intelligence** securely.  

### 1️⃣ Activate System-Assigned Managed Identity  
🔹 In the **Logic App settings**, enable **System-Assigned Identity**.  

🔹 **Where can you copy the Object (Principal) ID for later use?**  

✅ **Outcome**: The Logic App has an identity for authentication.  

---

## 🚀 Step 3: Assign Logic App Permissions  

💡 **Why?** The Logic App must have **access** to read from **Blob Storage** and write to **Storage Account**.  

### 1️⃣ Assign IAM Permissions to the Logic App  
🔹 Navigate to **Storage Account & Document Intelligence** → **Access Control (IAM)**  

🔹 Assign the following **roles** to the **Logic App Managed Identity**:  
✅ **Storage Blob Data Contributor**  
✅ **Storage Account Contributor**  
✅ **Cognitive Services Contributor** (For Document Intelligence)  

🔹 **Why are these roles important for document processing?**  

✅ **Outcome**: The Logic App can now access **Blob Storage** & **AI services**.  

---

## 🚀 Step 4: Configure the Logic App using the Azure Portal (Designer)  

💡 **Why?** You must **define the workflow** for processing incoming PDFs.  

### 1️⃣ Create the Workflow in the Logic App Designer  
🔹 Open **Logic App Designer** → Start with a **Blank Logic App**  

🔹 **Trigger:**  
✅ Add **"When a blob is added or modified (properties only)"**  
✅ **Select Storage Account**: `(Your Storage Account)`  
✅ **Select Container**: `Your-Container`  
✅ Add a **condition**: Trigger only for `.pdf` files  

🔹 **Processing Step:**  
✅ Add **"Analyze Document (Prebuilt-Invoice)"**  
✅ Provide **Storage URL** for the file  

🔹 **Save the Output:**  
✅ Add **"Create Blob"** in **Azure Blob Storage**  
✅ **Select Container**: `processed-json`  
✅ **Define Blob Name**:  

```plaintext
analyzed-document-@{triggerOutputs()?['body']['name']}.json
```

```plaintext
@body('Analyze_Document_for_Prebuilt_or_Custom_models_(v4.x_API)')
```

✅ **Outcome**: The Logic App will now process PDFs and save structured data in **Storage Account**.  

---

## 🚀 Step 5: (Alternative) Configure the Logic App using JSON Code  

✅ **Outcome**: The Logic App is now fully configured without using the Designer.  

---

## 🚀 Step 6: Create an Azure Data Factory (ADF)  

💡 **Why?** The ADF pipeline moves **PDFs** from **Fabric** to a **Storage Account**, triggering the Logic App.  

### 1️⃣ Create an ADF Instance  
🔹 Using **Azure Portal**, create an **Azure Data Factory instance**.  

🔹 **What authentication method should ADF use to access Fabric?**  

✅ **Outcome**: The ADF instance is now ready for pipeline creation.  

---

## 🚀 Step 7: Build the ADF Pipeline  

💡 **Why?** The pipeline ensures that **Fabric data** is automatically transferred to **Blob Storage**.  

### 1️⃣ Create a New Pipeline in ADF  
🔹 In **Azure Data Factory**, create a new **Copy Data pipeline**.  

🔹 **Source Configuration (Fabric Lakehouse)**  
✅ Select **Microsoft Fabric Lakehouse Files**  
✅ Set up **Linked Service** (Service Principal Authentication)  
✅ **Configure Folder Path**: `/Files/`  

🔹 **Destination Configuration (Azure Blob Storage)**  
✅ Select **Azure Blob Storage**  
✅ Set up **Linked Service**  
✅ **Configure Container**: `incoming-docs`  

🔹 **Run the Pipeline**  
✅ Click **Validate** → Ensure no errors  
✅ Click **Trigger Now**  

✅ **Outcome**: PDFs from **Fabric** are now **automatically copied** to **Blob Storage**, triggering the **Logic App**.  

---

## 🚀 Step 8: Verify Processed JSON Files in Storage Account  

💡 **Why?** The final output should be **structured JSON files** containing **extracted financial data**.  

### 1️⃣ Check Processed JSON Files  
🔹 Open **Azure Portal** → Navigate to **Your Storage Account Account**  
🔹 Locate the **processed-json container**  

🔹 **Are the JSON files present and correctly formatted?**  

✅ **Final Outcome**: AI-processed documents are saved in **Storage Account** for **fraud detection!** 🚀🔥  

## 🚀 Step 9: Create a new Lakehouse and move the JSON data to it from the Azure Storage account.

- Look for a way to get your analyzed JSON data into the new Lakehouse in Microsoft Fabric

### 🔹 Hints:  
- Logic App
- Fabric Copy Pipeline
- ADF Pipeline
- Manual Upload

---

## 🏁 Final Challenge Checkpoints  

✅ Does your **Logic App trigger** correctly when new PDFs arrive?  
✅ Can you confirm that **Document Intelligence extracts key data**?  
✅ Are the **structured JSON outputs** stored correctly in **Storage Account**?  
✅ Does the **ADF pipeline move PDFs** automatically from **Fabric to Blob Storage**?  

Once all steps are completed, you are ready to move on to the next challenge! 🚀  

---

## ❓ Troubleshooting Tips  

🔹 **If the Logic App does not trigger**, check if:  
   - The **Storage Account IAM roles** are properly assigned  
   - The **Blob Storage trigger condition** is correctly configured  

🔹 **If Document Intelligence fails**, verify:  
   - The **Cognitive Services Contributor** role is assigned  
   - The **Document Intelligence API key** and permissions are set correctly  

🔹 **If the ADF pipeline does not run**, check:  
   - The **Service Principal authentication** is properly configured  
   - The **Fabric workspace permissions** allow external access.