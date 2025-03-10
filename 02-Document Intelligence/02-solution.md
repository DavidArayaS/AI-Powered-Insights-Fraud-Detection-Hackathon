# 📖 Solution to challenge 2: Automating Document Processing with Logic Apps  

## 🔹 Objective  

In this challenge, you will:  

✅ Set up an Azure Logic App to process PDFs automatically  
✅ Enable Managed Identity and Assign Permissions to the Logic App  
✅ Use Document Intelligence (Form Recognizer) to analyze financial PDFs  
✅ Create an ADF pipeline to move PDFs from Fabric to a Storage Account  
✅ Store analyzed JSON outputs in Storage Account  
✅ Verify that all processed files are saved in JSON format in Storage Account  

---

## 🚀 Step 1: Create a Logic App  

### 1️⃣ Create a Logic App  
- Open **Azure Portal**  
- Search for **Logic Apps** → Click **+ Create**  
- Fill in the details:  
  - **Resource Group**: `YourUniqueResourceGroup`  
  - **Use the same region for all the resources you deployed already**
  - **Name**: `YourLogicApp`  
  - **Plan Type**: `Consumption`  
- Click **Review + Create** → **Create**  

---

## 🚀 Step 2: Enable Managed Identity for the Logic App  

### 1️⃣ Activate System-Assigned Managed Identity  
- Go to **YourLogicApp**  
- Click **Identity** (Left Menu)  
- Enable **System Assigned Identity**  
- Click **Save**  
- Copy the **Object (Principal) ID**  

✅ **Outcome**: The Logic App has an identity for authentication.  

---

## 🚀 Step 3: Assign Logic App Permissions  

- Go to your **Storage Account** **Storage Account** and **Document Intelligence** → Click **Access Control (IAM)**  
- Click **Add Role Assignment**  
- Assign the following roles to the **Logic App Managed Identity**:  
  ✅ **Storage Blob Data Contributor**  
  ✅ **Storage Account Contributor**  
  ✅ **Cognitive Services Contributor** (For Document Intelligence)  

✅ **Outcome**: The Logic App can read PDFs from Azure Blob Storage and write analyzed JSONs to Storage Account.  

---

## 🚀 Step 4: Configure the Logic App in the Azure Portal (Designer)  

- Open **YourLogicApp** → Click **Logic App Designer**  
- Click **Blank Logic App**  
- Click **+ Add Trigger** → Search for **Azure Blob Storage**  
- Select **When a blob is added or modified (properties only)**  
  - **Storage Account**: `Your Storage Account`  
  - **Container Name**: `incoming-docs`  
  - **Trigger Conditions**: `Ends with .pdf`  
  - **Interval**: `1 Minute`  

- Click **+ Add Step** → Search for **Document Intelligence (Form Recognizer)**  
- Select **Analyze Document (Prebuilt-Invoice)**  
  - **Storage URL**:  
    ```plaintext
    https://yourstoragename.blob.core.windows.net/incoming-docs/@{triggerOutputs()?['body']['name']}
    ```  

- Click **+ Add Step** → Search for **Azure Blob Storage**  
- Select **Create Blob**  
  - **Storage Account**: `Your Storage Account`  
  - **Container Name**: `processed-json`  
  - **Blob Name**:  
    ```plaintext
    analyzed-document-@{triggerOutputs()?['body']['name']}.json
    ```  
  - **Blob Content**:  
    ```plaintext
    @body('Analyze_Document_for_Prebuilt_or_Custom_models_(v4.x_API)')
    ```  
- Click **Save**  

✅ **Outcome**: The Logic App automatically analyzes PDFs and saves JSON outputs in Storage Account.  

---

## 🚀 Step 5: (Alternative) Use JSON Code for the Logic App  

If you want a faster approach, paste the following JSON into the **Logic App Code Editor** (modify as needed):  

[LogicApp.json]()

✅ Outcome: The Logic App will process PDFs and save JSONs without using the Designer.

---
## 🚀 Step 6: Create an Azure Data Factory (ADF)  

### 1️⃣ Create an ADF Instance  
- Open **Azure Portal** → Search for **Data Factory**  
- Click **+ Create**  
- Fill in the details:  
  - **Subscription**: Select your subscription  
  - **Resource Group**: `YourUniqueResourceGroup`  
  - **Region**: Same as Fabric  
  - **Name**: `YourADFInstance`  
- Click **Review + Create** → Click **Create**  

✅ **Outcome**: The ADF instance is created.  

---

## 🚀 Step 7: Create the ADF Copy Pipeline  

- Open **Azure Data Factory** → Click **Author & Monitor**  
- Click **+ New Pipeline**  
- Click **+ Add Activity** → Select **Copy Data**  

### 🔹 Configure the Source (Fabric Lakehouse)  
- Click **Source Tab** → Click **+ New**  
- Select **Microsoft Fabric Lakehouse Files**  
- **Linked Service**: Create a new Linked Service if needed  
- **Authentication**: `Service Principal`  
- Provide **Tenant ID, Client ID, Client Secret**  
- **Select Folder Path**: `/Files/`  
- Click **Save**  

### 🔹 Configure the Destination (Azure Blob Storage)  
- Click **Sink Tab** → Click **+ New**  
- Select **Azure Blob Storage**  
- **Container**: `Your Container`  
- Click **Save**  

### 🔹 Run the Pipeline  
- Click **Validate** → Ensure no errors  
- Click **Trigger Now**  
- Click *Publish*

✅ **Outcome**: PDFs are moved from Fabric to Azure Storage, triggering the Logic App.  

---

## 🚀 Step 8: Verify Processed JSON Files in Storage Account  

- Open **Azure Portal** → Go to **YourStorage AccountAccount**  
- Open `processed-json` → Verify JSON files  

✅ **Final Outcome**: Processed documents are saved in Storage Account for fraud detection! 🚀🔥  

## 🚀 Step 9: Create a new Fabric Lakehouse for the Analyzed JSON data

- Open Fabric → Click **Your Worskpace**  
- Click **+ New Item** 
- Select and Create a new **Lakehouse** for your analyzed data to be use in future stages of the solution you are building.  


## 🎯 Step 10: Challenge!!

- Look for a way to get your analyzed JSON data into the new Lakehouse in Microsoft Fabric

### 🔹 Hints:  
- Logic App
- Fabric Copy Pipeline
- ADF Pipeline
- Manual Upload

---