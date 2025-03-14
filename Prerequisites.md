# 🚀 AI-Powered Hackathon: Preparation Guide  

This hackathon is designed to be a **fun, collaborative, and hands-on learning experience**, bringing together **cutting-edge technologies** like **Microsoft Fabric, Azure, OpenAI**, and more to solve **real-world challenges**.

---

## 🔹 Preparing for the Hackathon  

To ensure you have the best possible experience, please review and complete all **prerequisites** before the event.  

---

## ✅ Personal Requirements  

Each participant must have:  

- 💻 **A laptop** with a modern web browser (**Chrome, Edge, Firefox, or Safari**).  
- 🐍 **Python 3.12 or later** → [Download here](https://www.python.org/downloads/)  
- 🖥 **Visual Studio Code** → [Download here](https://code.visualstudio.com/download)  

### 🔹 Optional Tools (Recommended)  
- ☁ **Azure Storage Explorer** → [Download here](https://azure.microsoft.com/en-us/products/storage/storage-explorer#Download-4)  
  *(Useful for managing Azure Storage resources efficiently)*  

---

## ✅ Azure Subscription & Access  

### 🔹 Subscription Requirements  
Participants must have access to an **Azure subscription** with the following:  

- **Shared Subscription or Resource Group** in your Company's Tenant (Dev, Test, SandBox): Ideally, your **team should leverage the same subscription or resource group** for seamless collaboration.  
- **RBAC Role**:  
  - At least **one team member** must have **Contributor + User Access Administrator** permissions.  
  - The rest of the team should have **Contributor access** to the subscription or a dedicated resource group.  
- **GitHub Codespaces (Optional)**: Ideally, each participant should have a **GitHub account** with access to create **Codespaces**.  

---

## ✅ Resource Provider Registration  

Ensure the following **resource providers** are registered within your Azure subscription:  

- `Microsoft.PolicyInsights`  
- `Microsoft.Cdn`  
- `Microsoft.StreamAnalytics`  

📌 **How to register**:  
- Navigate to **Azure Portal** → **Subscription Settings** → **Resource Providers**  
- Select each provider and **click Register**  

---

## ✅ Identity & Authentication  

### 🔹 Service Principal & Authentication  
Each team must create a **Service Principal (App Registration in Entra ID)** with:  

- ✅ **Client ID & Secret** (expires no earlier than **The Second Day of the Event**)  
- ✅ **Participants must have their Client ID and Secret available during the hackathon.**  

---

## ✅ Microsoft Fabric Prerequisites  

### 🔹 Fabric Access  
Participants can either:  
- **Create a new Microsoft Fabric Free Trial**, or  
- **Leverage an existing Fabric Capacity provisioned in their Azure Subscription**.  

### 🔹 Fabric Setup Requirements  
Each team must have:  
- ✅ **At least one team member assigned as a Microsoft Fabric Administrator**.  
- ✅ **A Microsoft Fabric Workspace assigned to the team**.  
- ✅ **The ability to create Lakehouses & Semantic Models in Fabric**.  
- ✅ **Access to Fabric Storage OneLake for file uploads**.  

---

## ✅ Azure OpenAI Requirements  

### 🔹 TPM Quota for OpenAI Models  
Check the **TPM quota** for your **Azure subscription** for the following **Large Language Models (LLMs)**:  

- `text-embedding-ada-002`  
- `gpt-35-turbo-16k`  

📌 **If the current quota is less than 100k**, request a **quota increase** before the event to ensure availability. Quota increases typically take **24 hours for approval**, so it is **critical to complete this step in advance**.  

- 🔹 **Check your current quota** → [Azure OpenAI Quota Guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/quota?tabs=rest)  
- 🔹 **Request a quota increase** → [Request Quota Increase](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu)  

---

## ✅ Network & Access Requirements  

### 🔹 Ensure **Unrestricted Access** to the Following Platforms:  

- 🌐 [**Azure AI Foundry**](https://ai.azure.com/)  
- 🏭 [**Azure Data Factory**](https://adf.azure.com/)  
- 📄 [**Document Intelligence Studio**](https://documentintelligence.ai.azure.com/)  
- ☁ [**Azure Portal**](https://portal.azure.com/)  
- 🔹 [**Microsoft Fabric**](https://app.fabric.microsoft.com/)  

---

## ✅ Visual Studio Code Requirements  

### 🔹 Required VS Code Extensions  
Teams must have **Visual Studio Code installed** with the following **extensions**:  

- 🐍 **Python**  
- 🔹 **Azure Tools**  
- 🧠 **Azure Semantic Kernel Tools**  

---

## 🎯 **What to Expect**  

- 🔥 **Hands-on technical challenges**  
- 🤝 **Collaboration with like-minded professionals**  
- 🧠 **Live problem-solving and expert guidance**  
- 🚀 **A chance to level up your skills and brainstorm use cases with our teams**  

---

## 🚀 **Final Checklist**  

✅ **Ensure all prerequisites are completed before the event.**  
✅ **Verify your access to Azure, Microsoft Fabric, and OpenAI services.**  
✅ **Confirm that you can access all necessary resources and tools.**  

---

## 🎉 **See You at the Hackathon!**  

We’re looking forward to an **engaging and inspiring event**—and most importantly, an **enjoyable learning journey for everyone!**  

**📩 If you have any questions or need assistance, feel free to reach out.**  

🚀 **Get ready to innovate, collaborate, and build AI-powered solutions!** 🎉  
