# 📖 Solution to Challenge 2: Automating Document Processing with Logic Apps  

## 🔹 Objective  

In this challenge, you will:  

✅ Set up an **Azure Logic App** to process PDFs automatically  
✅ Enable **Managed Identity** and assign permissions to the Logic App  
✅ Use **Document Intelligence (Form Recognizer)** to analyze financial PDFs  
✅ Create an **ADF pipeline** to move PDFs from Fabric to a Storage Account  
✅ Store **analyzed JSON outputs** in the Storage Account  
✅ Verify that all **processed files are saved in JSON format** in the Storage Account  

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

✅ **Outcome**: The Logic App now has an identity for authentication.  

---

## 🚀 Step 3: Assign Logic App Permissions  

- Go to your **Storage Account** and **Document Intelligence** → Click **Access Control (IAM)**  
- Click **Add Role Assignment**  
- Assign the following roles to the **Logic App Managed Identity**:  
  ✅ **Storage Blob Data Contributor**  
  ✅ **Storage Account Contributor**  
  ✅ **Cognitive Services Contributor** (For Document Intelligence)  

✅ **Outcome**: The Logic App can read PDFs from Azure Blob Storage and write analyzed JSONs to the Storage Account.  

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

![Logic App Designer](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/e024909d204fcec26d119ad58624d6d9fb2155b8/02-Document%20Intelligence/%7B8A2476E2-66BB-4D02-997C-5B06AD014A6C%7D.png)

## TIP: Storage Account Folder ID: **az storage container show --name --account-name**

✅ **Outcome**: The Logic App automatically analyzes PDFs and saves JSON outputs in the Storage Account.  

---

## 🚀 Step 5: (Alternative) Use JSON Code for the Logic App  

If you want a faster approach, paste the following JSON into the **Logic App Code Editor** (modify as needed):  

[LogicApp.json](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/98154b6420b02eed89954fd66f32afa9a3133da2/02-Document%20Intelligence/LogicApp.json)

✅ **Outcome**: The Logic App will process PDFs and save JSONs without using the Designer.  

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
- Click **Review + Create** → **Create**  

✅ **Outcome**: The ADF instance is created.  

---

## 🚀 Step 7: Create the ADF Copy Pipeline  

- Visit [adf.azure.com](https://adf.azure.com/) and connect to your ADF  
- Open **Azure Data Factory** → Click **Home**  
- Click **+ New Pipeline**  
- Click **+ Add Activity** → Select **Copy Data** and drag & drop it into the designer  

![ADF Pipeline](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/e024909d204fcec26d119ad58624d6d9fb2155b8/02-Document%20Intelligence/Reference%20Pictures/%7B3FF8B364-CF65-4CF6-BC4C-B6D9B7E90FBD%7D.png)

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/e024909d204fcec26d119ad58624d6d9fb2155b8/02-Document%20Intelligence/Reference%20Pictures/%7B95E116F7-6BE6-4D4F-AF17-D4827151274A%7D.png)

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/e024909d204fcec26d119ad58624d6d9fb2155b8/02-Document%20Intelligence/Reference%20Pictures/%7B232AD44C-4DB0-4DB9-8386-140BC0007BD2%7D.png)

### 🔹 Configure the Source (Fabric Lakehouse)  
- Click **Source Tab** → Click **+ New**  
- Select **Microsoft Fabric Lakehouse Files**  
- **Linked Service**: Create a new Linked Service if needed  
- **Authentication**: `Service Principal`  
- Provide **Tenant ID, Client ID, Client Secret** of the **Service Principal created for this event**  
- **Select Folder Path**: `/Files/`  
- Click **Save**  

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/e024909d204fcec26d119ad58624d6d9fb2155b8/02-Document%20Intelligence/%7BB0AA3853-7CA6-4E58-88E8-738BA2DCB7E1%7D.png)![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/e024909d204fcec26d119ad58624d6d9fb2155b8/02-Document%20Intelligence/%7B195003F0-C484-4AF8-9196-CAE5553E7D40%7D.png)

### 🔹 Configure the Destination (Azure Blob Storage)  
- Click **Sink Tab** → Click **+ New**  
- Select **Azure Blob Storage**  
- **Container**: `Your Container (used to store the analyzed JSON)`  
- Click **Save**  

![ADF Sink](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/e024909d204fcec26d119ad58624d6d9fb2155b8/02-Document%20Intelligence/%7B420F3069-08BC-42D3-AC23-8100EA769B71%7D.png)

### 🔹 Run the Pipeline  
- Click **Validate** → Ensure no errors  
- Click **Trigger Now**  
- Click **Publish**  

✅ **Outcome**: PDFs are moved from Fabric to Azure Storage, triggering the Logic App.  

---

## 🚀 Step 8: Verify Processed JSON Files in Storage Account  

- Open **Azure Portal** → Go to **Your Storage Account**  
- Open `processed-json` → Verify JSON files  

✅ **Final Outcome**: Processed documents are saved in the Storage Account for fraud detection! 🚀🔥  

---

## 🚀 Step 9: Create a New Fabric Lakehouse for the Analyzed JSON Data  

- Open **Microsoft Fabric** → Click **Your Workspace**  
- Click **+ New Item**  
- Select and create a **new Lakehouse** for your analyzed data to be used in future stages.  

---

## 🎯 Step 10: Challenge Time!!  

- **Find a way to get your analyzed JSON data into the your existing Lakehouse in Microsoft Fabric**  

### 🔹 Hints:  
- Logic App  
- Fabric Copy Job 
- ADF Pipeline  
- Manual Upload  

---