# 📖 Solution to Challenge 1: Setting Up Fabric & Storage Solutions.

## 🔹 Objective  
In this challenge, you will:  

✅ Set up Microsoft Fabric Capacity  
✅ Create a OneLake Lakehouse to store transaction PDFs  
✅ Upload the PDFs to OneLake  
✅ Create & Configure a Service Principal for authentication  
✅ Assign permissions in Fabric & Azure Blob Storage  

---

## 🚀 Step 1: Create Microsoft Fabric Capacity  

### 1️⃣ Create Fabric Capacity in Azure (skip if you already provisioned your Fabric Capacity or if you are using a free trial)

1. Go to **Azure Portal** → Microsoft Azure  
2. Search for **Microsoft Fabric** → Select **Fabric Capacity**  
3. Click **Create**  
4. Fill in the details:  
   - **Resource Group**: `YourUniqueResourceGroup`  
   - **Capacity Name**: `YourFabricCapacity`  
   - **SKU**: `F2` (minimum recommended)  
   - **Region**: Closest to your location  
   - **Security**: Enable **Private Link** (optional but recommended)  
5. Click **Review + Create**  
6. Wait for the deployment to complete.  

✅ **Best Practice**: Assign **Role-Based Access Control (RBAC)** to control access to the capacity.  

---

## 🚀 Step 2: Assign Fabric Capacity in Microsoft Fabric (skip if you already provisioned your Fabric Capacity or if you are using a free trial)  

### 1️⃣ Assign Fabric Capacity to Your Workspace  

1. Go to **Microsoft Fabric**  
2. Click **Admin Settings** (⚙️ gear icon) → **Fabric Capacity**  
3. Click **Assign Capacity**  
4. Select the Fabric Capacity you created (`YourFabricCapacity`)  
5. Click **Save**  

✅ **Outcome**: Your Fabric workspace is now connected to Microsoft Fabric Capacity.  

---

## 🚀 Step 3: Create a OneLake Lakehouse  

### 1️⃣ Create a new Fabric Workspace

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/cbc097fda45d32090f4d726b4fde8dc7ff3ba5ee/01-Data%20Ingestion/Reference%20Pictures/%7B57FFD2F6-A926-4079-A0A7-8CE696F2B0E5%7D.png)

1. In **Microsoft Fabric**, go to your **Workspace**  
2. Click **+ New item** → Select **Lakehouse**  

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/cbc097fda45d32090f4d726b4fde8dc7ff3ba5ee/01-Data%20Ingestion/Reference%20Pictures/%7B55843AA2-7852-48F4-9FF3-7A32BD832729%7D.png)

3. Fill in the details:  
   - **Name**: `YourLakehouse`  
   - **Description**: Storage for Financial PDFs  
   - Click **Create**  
   - **Security**: Assign **Admin & Reader** permissions  

✅ **Best Practice**: Keep a **structured folder hierarchy** in OneLake for organized data.  

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

### 1️⃣ Create an Azure Storage Account  

1. Go to **Azure Portal** → Search for **Storage Accounts**  
2. Click **+ Create**  
3. Fill in the details:  
   - **Resource Group**: `YourUniqueResourceGroup`  
   - **Storage Account Name**: `yourstorageaccount`  
   - **Region**: Same as Fabric  
   - **Performance**: **Standard**  
   - **Replication**: **Locally Redundant Storage (LRS)**  
4. Click **Review + Create** → Click **Create**  

---

## 🚀 Step 6: Create a Standard LRS Storage Account  

💡 **Why?** This separate **Storage Account** will be used to store structured data outputs.  

### 1️⃣ Create a Storage Account  

1. Open **Azure Portal** → Search for **Storage Accounts**  
2. Click **+ Create**  
3. Fill in the details:  
   - **Resource Group**: `YourUniqueResourceGroup`  
   - **Storage Account Name**: `yourstorageaccount`  
   - **Region**: Same as Fabric  
   - **Performance**: **Standard LRS**  
   - **Replication**: **Locally Redundant Storage (LRS)**  
4. Click **Review + Create** → Click **Create**  

### 2️⃣ Create a Container with a Folder Inside  

1. Navigate to your Storage Account  
2. Click **Data Storage** → Select **Containers**  
3. Click **+ Add** → Name the container: `container`  
4. Click **Create**  
5. **Add a folder for storing the analyzed JSON data**  

---

## 🚀 Step 7: Create an Azure Document Intelligence Instance  

💡 **Why?** **Azure Document Intelligence (Form Recognizer)** is required for **AI-powered document processing**.  

### 1️⃣ Create a Document Intelligence Instance  

1. **Go to** [Azure Portal](https://portal.azure.com) → Search for **Document Intelligence**  
2. Click **+ Create**  
3. Fill in the details:  
   - **Resource Group:** `YourUniqueResourceGroup`  
   - **Name:** `YourDocumentIntelligenceInstance`  
   - **Region:** Same as Fabric  
   - **Pricing Tier:** `S0` *(Standard - recommended)*  
4. Click **Review + Create** → Click **Create**  
5. Wait for the deployment to complete.  

### 2️⃣ Retrieve API Key & Endpoint  

1. **Go to** the **Document Intelligence Resource**  
2. Navigate to **Keys and Endpoints**  
3. **Copy & Save** the following:  
   - **Endpoint URL**  
   - **Primary Key**  

✅ **Outcome:** The **Document Intelligence instance** is ready for AI document processing.  

---

## 🚀 Step 8: Create & Configure a Service Principal (skip this step if the Service Principal was created as suggested in the prerequisites email)  

### 1️⃣ Create a Service Principal in Azure Entra ID  

1. Go to **Azure Entra ID (Active Directory)**  
2. Click **App Registrations** → **+ New Registration**  
3. Fill in:  
   - **Name**: `YourServicePrincipal`  
   - **Supported Account Type**: **Single Tenant**  
4. Click **Register**  
5. Copy the following details:  
   - **Application (Client) ID**  
   - **Tenant ID**  

---

## 🚀 Step 9: Generate & Store Service Principal Credentials (skip this step if the Service Principal was created as suggested in the prerequisites email)  

### 1️⃣ Create Client Secret  

1. Go to **Azure Entra ID** → **App Registrations**  
2. Select **YourServicePrincipal**  
3. Go to **Certificates & Secrets** → **+ New Client Secret**  
4. Set **Expiration**: **1 Month** (or as per security policy)  
5. Copy & Save the **Secret Value** (*It will not be visible again!*)  

✅ **Outcome**: You now have **Client ID, Tenant ID, and Secret Key** for authentication.  

---

## 🚀 Step 10: Assign Permissions in Fabric & Blob Storage  

### 1️⃣ Enable Service Principal Authentication in Fabric  

1. Go to **Microsoft Fabric** → **Fabric Portal**  
2. Click **Admin Settings** (⚙️ gear icon) → **Admin Portal**  
3. Enable **Service Principals can use Fabric APIs**  
4. Click **Save**  

✅ **Outcome**: The Service Principal can now access **Fabric APIs**.  

### 2️⃣ Assign Permissions in Storage Account  

1. Go to your **Storage Account** → Click **Access Control (IAM)**  
2. Click **Add Role Assignment**  
3. Assign the following roles to **YourServicePrincipal**:  
   ✅ **Storage Blob Data Contributor**  
   ✅ **Storage Account Contributor**  
   ✅ **Cognitive Services Contributor** *(For Document Intelligence)*  
4. Click **Save**  

✅ **Outcome**: The **Service Principal has full access** to Fabric & Blob Storage.  