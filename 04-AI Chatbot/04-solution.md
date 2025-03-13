# 📖 Solution to Challenge 04: Setting Up LLMs for a Chatbot and the Resources Needed

## 🔹 Objective 
In this challenge, you will:

✅ Create, Define, and Explore LLMs for a Chatbot and the Resources Needed to Set Up the Same.  
✅ Add Data to Your Project and Explore the Response of Chatbot Post Indexing and Grounding.  
✅ Build & Customize - Create, Iterate, and Debug Your Orchestration Flows.

---

## 🚀 Generic TIPS:

- Try to keep all resources and RG in the same Region for ease of understanding and standardization.
- Most companies have organizational policies on auto-creation of Key Vault & Storage account, so here we will be creating all resources separately and will stitch them together.
- Add a tag to the Resources and resource group when you create them so that we can identify them later for cost management or other aspects.
- Ensure that all necessary resource providers are registered. For example, you might need to register Microsoft.PolicyInsights and Microsoft.Cdn policies by selecting them and clicking the register button in the Azure Portal.
- Make sure the location or region for each of the resources is preferably one of the following, this will ensure smooth testing of all resources:
  - Australia East
  - Canada East
  - East US
  - East US 2
  - France Central
  - Japan East
  - North Central US
  - Sweden Central
  - Switzerland
- Check the TPM quota for your subscription for the LLMs `text-embedding-ada-002` and `gpt-35-turbo-16k`. If you are already familiar with the same, request a quota addition if the current quota is in the 2-digit range (10k-90k) and increase it to whatever is maximum for each model.

---

## 🚀 Milestone #1: Create, Define, and Explore LLMs for a Chatbot and the Resources Needed to Set Up the Same

### 1️⃣ Create the Resource Group (RG)
1. Sign in to the Azure portal.  
2. Select **Resource groups**.  
3. Select **Create**.  
4. Enter the following details:
   - **Subscription**:
   - **Resource group**:
   - **Region**:
5. Select **Review + Create**.

![Create Resource Group](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/1.png)

---

### 2️⃣ Create/Use the existing Storage account (this will be source of our custom data)

**TIP**: The source of your data can be Fabric or Data Lake Gen2 from the previous challenges, but that will involve some additional steps to fulfill and might require some extra efforts to set the same up.  
Since we are time bound, we will just use the Dimension Xls (which will be converted to csv/txt here) for the purpose of this challenge. If you were able to successfully finish the first 3 challenges, you already have 3 Dim xls files with you in Fabric Lakehouse and can convert the files to CSV (using a dataflow to transform, then a data copy pipeline to copy from Fabric to the new storage account) and upload them into the storage account we are going to create below.

First, use a dataflow Gen2 transformation on the files.  
Second step is to convert the transformed files to csv using the snippet in a notebook:

```python
# Import necessary libraries
import pandas as pd
import os

# Define the source and destination paths
source_folder = "/lakehouse/default/Tables/container"
destination_folder = "/lakehouse/default/Files"

# Loop through all files in the source folder
for file_name in os.listdir(source_folder):
    if file_name.endswith(".xls") or file_name.endswith(".xlsx"):
        # Read the Excel file
        xls_file_path = os.path.join(source_folder, file_name)
        df = pd.read_excel(xls_file_path)

        # Define the CSV file path
        csv_file_name = file_name.replace(".xls", ".csv").replace(".xlsx", ".csv")
        csv_file_path = os.path.join(destination_folder, csv_file_name)

        # Save the DataFrame as a CSV file
        df.to_csv(csv_file_path, index=False)

        print(f"Converted {file_name} to {csv_file_name} and saved to {destination_folder}")
```

Once the conversion is completed you can use a data factory copy job to copy from fabric to the new storage account (Please follow the steps in challenge 2 to complete this task)  
Or the Alternative option is to manually do it, for keeping the challenge simple we suggest following this alternative solution.  
Get the xls files and save them locally in txt format or csv format and save them inside a subfolder. This folder can be uploaded to the parent container inside our storage account once the storage account creation steps are completed.

**Reason to go with manual upload**: Since the Excel sheet we have created during the last process might have some different formatting it is always better to upload a folder of all the files saved in `.txt` format and upload directly to the storage account container in-order to save time.  
The reason for not to use `.xls` as source data or for data transformation is since the formatting is key and any change or problems in the file inside any columns will result in failure of recognizing the file.

1. On the **Storage accounts** page, select **Create**.  
2. Fill in the required details.  
3. Enter the following details:
   - **Subscription**:
   - **Resource group**:
   - **Storage account name**:
   - **Region**:
   - **Performance**: Select Standard
   - **Redundancy**: LRS
   - **Networking**: Enable public access from all networks (this will help avoid isolated environment-specific networking issues)
   - Keep everything else default.
4. Select **Review + Create**.  
5. Click **Create**.  

![Create Storage Account](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/2.png)

6. Once the storage account is created, create a container `refined-data` and upload all 4 csv files into the container (inside a folder with the name `csv-data` or `txt-data`), so that at the end of the activity you will have a storage account with a container inside, and a subfolder inside that container with all the files in CSV format. Once everything is done, it will look like below:

![Container with CSV Files](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/3.png)

---

### 3️⃣ Create the Key Vault
1. On the **Key Vault** page, select **Create**.  
2. Fill in the required details.  
3. Enter the following details:
   - **Subscription**:
   - **Resource group**:
   - **Key Vault Name**:
   - **Region**:
   - **Pricing tier**: Standard
   - Keep everything else default.
4. Select **Review + Create**.  
5. Click **Create**.

![Key Vault Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/kv4.png)

---

### 4️⃣ Create a Search Service Connection to Index the Sample Product Data
1. On the home page, select **+ Create a resource** and search for **Azure AI Search**. Then create a new Azure AI Search resource with the following settings:
   - **Subscription**:
   - **Resource group**:
   - **Service name**:
   - **Location**: Make a random choice from any of the regions mentioned in the Tips.
   - **Pricing tier**: Standard
   - **Scale**: Increase the search unit by 4 to improve query performance.
2. Wait for your Azure AI Search resource deployment to be completed.

![Azure AI Search Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/search5.png)

---

### 5️⃣ Create an Azure AI Service
1. On the home page, select **+ Create a resource** and search for **Azure AI Services**. Then create a new Azure AI Service resource with the following settings:
   - **Subscription**:
   - **Resource group**:
   - **Region**: Make a choice from any of the regions mentioned in the Tips.
   - **Name**:
   - **Pricing tier**: Standard
   - **Scale**: Increase the search unit by 4 to improve query performance.
2. Wait for your Azure AI Service resource deployment to be completed.

![Azure AI Services Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/aiservice6.png)

**Remarks**: At this point, all the resources needed to build a Hub and Project inside a Hub in AI Foundry are completed.

---

### 6️⃣ Create a Hub
1. On the Ai Foundry page in [https://portal.azure.com], select **+ Create** and select **Hub**. Then create a new Hub resource with the following settings:
   - **Subscription**:
   - **Resource group**:
   - **Region**: Make a choice from any of the regions mentioned in the Tips.
   - **Name**:
   - **Connect AI Services incl. OpenAI**: Select the AI service we created earlier from the drop-down.
   - **Storage Tab**: Select the storage account we created earlier.
   - **Key Vault Tab**: Select the key vault we created earlier.
   - **Networking**: Keep the default (public).
   - Rest all keep the default.
   - Click **Create + Review**, and then **Create**.
2. Wait for your Azure AI Hub resource deployment to be completed.

![Hub Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/hub7.png)

---

### 7️⃣ Create a Project
1. On the Ai Foundry page in [https://portal.azure.com], select **+ Create** and select **Project**. Then create a new Project resource with the following settings:
   - **Subscription**:
   - **Resource group**:
   - **Region**: Make a choice from any of the regions mentioned in the Tips.
   - **Name**:
   - **Hub**: Select the Hub we just created in the step before this.
   - Rest all keep the default.
   - Click **Create + Review**, and then **Create**.
2. Wait for your Azure AI Project resource deployment to be completed.

![Project Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/project8.png)

**Remarks**: This should not take more than 20 minutes to build. Now we shift to the AI Foundry page. Go to [https://ai.azure.com]. Select the project and we will be working inside this going forward.

**TIP**: If there are no organizational policies and constraints applied to any subscription, you can directly sign up at [https://ai.azure.com] and create the project. While doing so, all other resources will also be created. You just need an AI search service resource to be created beforehand.

---

### 8️⃣ Deploy Models
You need two models to implement your solution:
- An embedding model to vectorize text data for efficient indexing and processing.
- A model that can generate natural language responses to questions based on your data.

a. In the Azure AI Foundry portal, in your project, in the navigation pane on the left, under **My assets**, select the **Models + endpoints** page.  
b. Create a new deployment of the `text-embedding-ada-002` model with the following settings by selecting **Customize** in the Deploy model wizard:
   - **Deployment name**: text-embedding-ada-002
   - **Deployment type**: Standard
   - **Model version**: Select the default version
   - **AI resource**: Select the resource created previously
   - **Tokens per Minute Rate Limit (thousands)**: Slide it to maximum
   - **Content filter**: DefaultV2
   - **Enable dynamic quota**:  
   > **Note**: If your current AI resource location doesn’t have quota available for the model you want to deploy, you will be asked to choose a different location where a new AI resource will be created and connected to your project.

c. Repeat the previous steps to deploy a `gpt-35-turbo-16k` model with the deployment name `gpt-35-turbo-16k` (if you are curious you can try some latest gpt models also).  
d. Select the `gpt-35-turbo-16k` model, and click on **Open in playground**.  
e. Test the chatbot with a question "What do you do?" and check the response.  
f. Now change the model instructions and context message to the following:

![Model Instructions](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/model9.png)

**Objective**: Assist users with financial-related inquiries, offering insights, advice, and recommendations as a knowledgeable financial advisor.  
**Capabilities**:
- Provide up-to-date financial information, including market trends, investment options, and financial products.
- Offer personalized financial advice based on user preferences, risk tolerance, and financial goals.
- Share tips on budgeting, saving, and managing financial risks.
- Help with financial planning, including retirement planning, tax strategies, and wealth management.
- Answer common financial questions and provide solutions to potential financial issues.

**Instructions**:
1. Engage with the user in a friendly and professional manner, as a financial advisor would.
2. Use available resources to provide accurate and relevant financial information.
3. Tailor responses to the user's specific financial needs and interests.
4. Ensure recommendations are practical and consider the user's financial safety and comfort.
5. Encourage the user to ask follow-up questions for further assistance.

g. Select **Apply changes**.  
h. Test the chatbot with the question "What do you do?" You will get a response specific to the new context. The same question asked before the context change would have been very generic.

---

### Milestone #1: Define & Explore
You can test the model by going into the playground and chatting with the model. Ask some generic questions, and it will give you generic answers. At this point, the model is looking for data it was trained on and is not grounded with custom data. We were also able to customize the model instructions and context by adding more specific data for responding to user questions.

---

### Milestone #2: Add Data to Your Project and Explore the Response of Chatbot Post Indexing and Grounding

1. **Enable Managed Identity**  
   a. Enable MI for both AI service and AI search service.  
   b. On the browser tab for the Search service resource in the Azure portal, enable the managed identity:
      - From the left pane, under **Settings**, select **Identity**.
      - Switch **Status** to **On**.
      - Select **Save**.  
   c. On the browser tab for the Azure AI services resource in the Azure portal, enable the managed identity:
      - From the left pane, under **Resource Management**, select **Identity**.
      - Switch **Status** to **On**.
      - Select **Save**.

2. **Set API Access Control for Search**  
   a. On the browser tab for the Search service resource in the Azure portal, set the API Access policy:
      - From the left pane, under **Settings**, select **Keys**.
      - Under **API Access control**, select **Both**.
      - When prompted, select **Yes** to confirm the change.

3. **Assign Roles**  
   a. The general pattern for assigning role-based access control (RBAC) for any resource is:
      - Navigate to the Azure portal for the given resource.
      - From the left page in the Azure portal, select **Access control (IAM)**.
      - Select **+ Add > Add role assignment**.
      - Search for the role you need to assign and select it. Then select **Next**.
      - When assigning a role to yourself:
        - Select **User, group, or service principal**.
        - Select **Select members**.
        - Search for your name and select it.
      - When assigning a role to another resource:
        - Select **Managed identity**.
        - Select **Select members**.
        - Use the dropdown to find the type of resource you want to assign. For example, Azure AI services or Search service.
        - Select the resource from the list that appears. There might only be one, but you still need to select it.
      - Continue through the wizard and select **Review + assign** to add the role assignment.
   
   b. Use these steps to assign roles for the resources you're configuring in this tutorial:
      - Assign the following roles on the browser tab for Search service in the Azure portal:
        - **Search Index Data Reader** to the Azure AI services managed identity
        - **Search Service Contributor** to the Azure AI services managed identity
        - **Contributor** to yourself (to find Contributor, switch to the Privileged administrator roles tab at the top. All other roles are in the Job function roles tab.)
      - Assign the following roles on the browser tab for Azure AI services in the Azure portal:
        - **Cognitive Services OpenAI Contributor** to the Search service managed identity
        - **Contributor** to yourself (if not already in place)
      - Assign the following roles on the browser tab for Azure Blob storage in the Azure portal:
        - **Storage Blob Data Contributor** to the Azure AI services managed identity & Azure AI services managed identity
        - **Contributor** to yourself (if not already in place)

> **TIP**: If you are using identity-based authentication, "Storage Blob Data Contributor", "Storage File Privileged Contributor" (Inside Storage account resources) and "Cognitive Services OpenAI Contributor" (Inside AI services resource) roles must be granted to individual users that need access on the storage account.

4. **Storage Account Datastore Configuration**  
   a. The best practice is to use Microsoft Entra Authentication  
   b. Enable the Account Key for the storage account and make sure we can gather the information for later (use this only if #a is not an option)

> **TIP**: You have other options like SAS URL creation, Entra ID authentication. For simplicity, we are choosing Entra ID authentication in the below steps.

### 5. Create Connections to the Blob Storage & AI Search

   a. We have multiple ways to achieve this, but the best way is to go to the Management Center in [ai.azure.com] or go to [ml.azure.com] and create connections under **Connected resources**. Add a new connection.  
   b. Add the Azure AI Search as an internal connection.

   c. For loading the custom data (if you are not uploading the files/folder directly to the AI Foundry), you can establish the connection as per your use case. Since we are time-bound and want to ensure everyone can follow (those with organizational constraints and other Entra ID restrictions), we will use Azure Blob storage:
      1. Click on **+ New connection**.
      2. Select **Blob storage** from the Data sublist.
      3. Select the subscription ID, storage account, and blob container (the parent container).

      **Option 4#a**:
      4. Under authentication method, select **Microsoft Entra ID based**.
      5. Give the connection a name, and save it.

      **Option 4#b**:
      4. Under authentication method, select **Credential based**.
      5. Under authentication type, select **Account key**, paste the earlier copied storage account key, give the connection a name, and save it.

![Connection to Blob Storage](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/conn10.png)

---

### 6. Add the Custom Data to AI Foundry

a. Go to your project in Azure AI Foundry.  
b. Select **Data + Indexes**.  
c. Select **+ New Data**.  
d. Select the data source from the drop-down (the same connection we created in the previous step). It will take a bit, and if everything is right, it will enable the option of **Browse to storage path**. If any access issue or key issue is there, it won't enable this option and instead will enable the **Enter storage path manually** only. This is a sign to troubleshoot the issue.  
e. Select the subfolder inside the main folder and click **Next**.  
f. Give the data a name so you can recognize it.

![Data Addition in AI Foundry](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/data11.png)

g. Once created, make sure the data is readable and displayed with the number of files and total size updated. In the preview, you can see the files you have uploaded.

h. Now we will go ahead and create the Index for the already connected custom data:
1. Go to **Indexes**.
2. Click on **+ New Index**.
3. Select the Data Source (we have to select **Data** in AI Foundry since we already established the connection and created the data).
4. Select the data we created in the previous step.
5. Select the Index configuration, the AI Search service name, then give the vector index the name you want to give. Compute is auto-selected; if you want better performance, you can select a higher-value compute.
6. Select the AOAI Service connection which got created when we created the project.
7. Create vector index.
8. In the status, you can see that your data ingestion is in progress. This process might take several minutes. Before proceeding, wait until you see the data source and index name in place of the status.

![Creating a Vector Index](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/vector12.png)

> **TIP**: If you're curious about the steps happening on the back end, click on the job details, and it will take you to [https://ml.azure.com](https://ml.azure.com) and show all the jobs and steps it is running for vector indexing. This will take a lot of time depending on the number of documents you have and the type of resources and limits you use on all the components involved in this step.

![Vector Indexing Status](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/vector13.png)

---

### 7. Add Your Custom Data to Your Chat Model

a. Go to your project in Azure AI Foundry.  
b. Select **Playgrounds** and **try the chat playground**.  
c. Select **Add your data**.  
d. Select the available project index, the one we created in the last step.  
e. Search type: leave it as hybrid.  
f. No other changes; this chatbot is ready to test with custom data.  
g. This is ready to test. Refresh the page, give it a minute, and then test some specific questions like:
   - what is the Address of ADDR-29841?
   - what is the ApplicationID of the customer CLI-19708?
   - how many clients does Wayne Enterprises company have?
   - how many addresses are from texas?
   - can you list down all the address ID for the addresses from texas?

Congratulations!  
You have now trained the model with your own data, and it is ready to serve you with domain-specific answers. There are two things to notice:
- If you are uploading data in txt format, the answers will be much better.
- If you are using csv, the answers might be inconsistent.

Milestone #4 will solve these problems with an AI agent.

If you used csv data as the source, you can upload the data, create an index, and vectorize the data using txt files to check the results. This approach will yield better results than using csv files.

You will also notice that the app can quickly retrieve individual details. However, it struggles with bulk responses. This is a limitation of the current configuration, which is why more frameworks and customization are needed to make the application more powerful.

### Milestone #2: Result

Build & Customize - Generative AI app that uses your own custom data. You can now chat with the model asking the same question as before, and this time it uses information from your data to construct the response. You can expand the references button to see the data that was used.

---

### Milestone #3: Build & Customize - Create, Iterate, and Debug Your Orchestration Flows

**Context**: The sample prompt flow you are using implements the prompt logic for a chat application in which the user can iteratively submit text input to the chat interface. The conversational history is retained and included in the context for each iteration. The prompt flow orchestrates a sequence of tools to:  
1. Append the history to the chat input to define a prompt in the form of a contextualized question.  
2. Retrieve the context using your index and a query type of your own choice based on the question.  
3. Generate prompt context by using the retrieved data from the index to augment the question.  
4. Create prompt variants by adding a system message and structuring the chat history.  
5. Submit the prompt to a language model to generate a natural language response.

#### 1. Save the Current Prompt Flow

a. In the Azure AI Foundry portal, in your project, in the navigation pane on the left, under **Playgrounds**, open the chat model.  
b. Choose **prompt flow** and save the current prompt flow with the name "default-flow".  
c. Once it is created, go and check out the flow and what all components are there by default. In the next step, we will be cloning a new flow model so that the chat will have history.

#### 2. Use the Index in a Prompt Flow

a. Your vector index has been saved in your Azure AI Foundry project, enabling you to use it easily in a prompt flow.  
b. In the Azure AI Foundry portal, in your project, in the navigation pane on the left, under **Build and customize**, select the **Prompt flow** page.  
c. Create a new prompt flow by cloning the **Multi-Round Q&A on Your Data** sample in the gallery.  
d. Save your clone of this sample in a folder named **product-flow**.  
e. Use the **Start compute session** button to start the runtime compute for the flow. Wait for the runtime to start. This provides a compute context for the prompt flow.  
f. In the **Inputs** section, ensure the inputs include:
   1. chat_history
   2. chat_input

The default chat history in this sample includes some conversation about AI.

g. In the **Outputs** section, ensure that the output includes:
   1. chat_output with value `${chat_with_context.output}`

h. In the **modify_query_with_history** section, select the following settings (leaving others as they are):
   1. Connection: The default Azure OpenAI resource for your AI hub
   2. Api: chat
   3. deployment_name: gpt-35-turbo-16k
   4. response_format: `{"type":"text"}`

i. Wait for the compute session to start, then in the **lookup** section, set the following parameter values:
   1. mlindex_content: Select the empty field to open the Generate pane
      - index_type: Registered Index
      - mlindex_asset_id: `<name of your vector index>:1`
      - save
   2. queries: `${modify_query_with_history.output}`
   3. query_type: Hybrid (vector + keyword)
   4. top_k: 2

j. In the **generate_prompt_context** section, review the Python script and ensure that the inputs for this tool include the following parameter:
   1. search_result (object): `${lookup.output}`

k. In the **Prompt_variants** section, review the Python script and ensure that the inputs for this tool include the following parameters:
   1. contexts (string): `${generate_prompt_context.output}`
   2. chat_history (string): `${inputs.chat_history}`
   3. chat_input (string): `${inputs.chat_input}`

l. In the **chat_with_context** section, select the following settings (leaving others as they are):
   1. Connection: Default_AzureOpenAI
   2. Api: Chat
   3. deployment_name: gpt-35-turbo-16k
   4. response_format: `{"type":"text"}`

Then ensure that the inputs for this tool include the following parameters:
   5. prompt_text (string): `${Prompt_variants.output}`

m. On the toolbar, use the **Save** button to save the changes you’ve made to the tools in the prompt flow.  
n. On the toolbar, select **Chat**. A chat pane opens with the sample conversation history and the input already filled in based on the sample values. You can ignore these.  
o. In the chat pane, replace the default input with the question `how many clients does Wayne Enterprises company have?` and submit it.  
p. Review the response, which should be based on data in the index.  
q. Review the outputs for each tool in the flow.  
r. In the chat pane, enter the question: `what is the status of the client with ClientId CLI-28048?`.
    what is the Address of ADDR-29841?
    what is the ApplicationID of the customer CLI-19708?
    Is the loan approved?
    how many clients does Wayne Enterprises company has?
    how many addresses are from texas?
    can you list down all the address ID for the addresses from texas?

s. Review the response, which should be based on data in the index and take into account the chat history (so “there” is understood as what you have mentioned before).  
t. Review the outputs for each tool in the flow, noting how each tool in the flow operated on its inputs to prepare a contextualized prompt and get an appropriate response.

#### 3. Deploy the Flow

a. On the toolbar, select **Deploy**.  
b. Create a deployment with the following settings:
1. Basic settings:
   - Endpoint: New
   - Endpoint name: Use the default unique endpoint name
   - Deployment name: Use the default deployment endpoint name
   - Virtual machine: Standard_DS3_v2
   - Instance count: 3
   - Inferencing data collection: Selected
2. Advanced settings:
   - Use the default settings

c. In the Azure AI Foundry portal, in your project, in the navigation pane on the left, under **My assets**, select the **Models + endpoints** page.  
d. Keep refreshing the view until the new-endpoint-de deployment is shown as having succeeded under the new-endpoint endpoint (this may take a significant period of time).  
e. When the deployment has succeeded, select it. Then, on its **Test** page, review the response.  
f. Enter the prompt with a follow-up question and review the response.  
g. View the **Consume** page for the endpoint, and note that it contains connection information and sample code that you can use to build a client application for your endpoint — enabling you to integrate the prompt flow solution into an application as a custom copilot.

Congratulations! You have now trained the model with your own data and created a new prompt flow where the user can iteratively submit text input to the chat interface. The conversational history is retained and included in the context for each iteration.

### Milestone #3: Result

The sample prompt flow you are using implements the prompt logic for a chat application in which the user can iteratively submit text input to the chat interface. The conversational history is retained and included in the context for each iteration. With this, the challenge #3 is completed; we still have not solved the problem of bulk response query or rather SQL-formatted queries in human language. Hungry for more? Let’s explore further!

---

### Milestone #4: Query multiple CSV files using Azure OpenAI & Langchain framework

**Context**: At the end of Milestone #2, we saw we were able to ask specific questions (like individual details), but when it comes to SQL-formatted queries in human-readable form, the chat application is not functioning well.  
The reason is that the chat prompt is not autonomous, and when the source data is too large (like in our case) or it is semi-structured data like CSV or Excel, it does not function well. That is where this milestone comes in.  
We can combine the AI Agent and OpenAI, and we get a very powerful, flexible autonomous system which can calculate and query complex questions in human-readable format.

#### 1. Create an Azure OpenAI resource from the portal
1. Sign in to the Azure portal.  
2. Select/Search **Azure OpenAI**.  
3. Select **+Create**.  
4. Enter the following details:
- **Subscription**:
- **Resource group**:
- **Region**:
- **Name**:
- **Pricing tier**: Standard S0
5. Keep the rest all default.  
6. Select **Review + Create**.  
7. Once the deployment is completed go to the resource and check the keys and endpoints; we will need those for later purposes.  
8. Click on **Go to Azure AI Foundry portal**, and the rest of the work will be done in the Foundry portal.

![Azure OpenAI Resource Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/openai14.png)

### 2. Deploy Model
You need a model to implement your solution:
- A model that can generate natural language responses to questions based on your data.

a. In the Azure AI Foundry portal, in your Azure OpenAI resource, in the shared resources pane on the left, under **Deployments**, under the **Model deployments** select the **Deploy base model** page.  
b. Create a new deployment of the `gpt-35-turbo-instruct` model with the following settings by selecting **Customize** after the **Confirm** button is pressed, in the Deploy model wizard:
- **Deployment name**: gpt-35-turbo-instruct
- **Deployment type**: Standard
- **Model version**: Select the default version
- **Resource location**: Keep the default value
- **Tokens per Minute Rate Limit (thousands)**: Slide it to maximum
- **Enable dynamic quota**:

Then click on **Create resource and deploy**.  
> **Note**: If your current AI resource location doesn’t have quota available for the model you want to deploy, you will be asked to choose a different location where a new AI resource will be created and connected to your project.

c. Test the chatbot with a question "What do you do?" and check the response.

Now we will go to the base machine from which we are working, so that this OpenAI service can be connected to our CSV and enable it so that we can talk to this CSV in human-readable format and get a response.

**TIP**: We will be using VSCode as our code editor, and it will be awesome if you have the following extensions installed:
```markdown
Azure Account  
Azure CLI Tools  
Azure Developer CLI  
Azure Machine Learning  
Jupyter  
Jupyter Notebook Renderers  
jupyter-notebook-vscode  
Linter  
Pylance  
Python  
Python Debugger  
Python snippets


## At this point using the VScode terminal make sure you are connecting into the Azure environment 
you can use  

- azd auth login **If Azure developwe CLi is not installed we can install it provided we have admin rights on the laptop**

### 3. Write the python Code using Langchain framework and read the csv from storage account ,combine and get it ready for querying using an agent,deploy an agent and invoke the agent to get answers

1. Install the various python packages we will be using during this coding session.open up a new file with .ipynb extension,this will help us run the code in cells and seperate functions ,this is better for troubleshooting and learning the python coding also

```python
%pip install openai
%pip install langchain
%pip install pandas
%pip install langchain_experimental
%pip install langchain_openai
%pip install tabulate
%pip install azure-storage-blob
```

2. Import the needed packages

```python
import openai
print(openai.__version__)
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient
```

3. Connect to the Azure subscription, gather the details, get the CSV files in a loop, and combine them together using dataframes and place it in a single file

```python
connection_string = "<<connectionstrong of your storage account>>"
container_name = "refined-data"
blob_names = ["DimAddress.csv", "DimApplicant.csv", "DimClient.csv", "factfinancial.csv"]
# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
dataframes = []
for blob_name in blob_names:
    blob_client = container_client.get_blob_client(blob_name)

    # Download the blob content
    blob_content = blob_client.download_blob().content_as_text()

    # Read the content into a pandas DataFrame
    df = pd.read_csv(StringIO(blob_content))
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
print(combined_df.head())
```
4. Save the combined DataFrame to a CSV file

```python
combined_csv_path = "combined.csv"
combined_df.to_csv(combined_csv_path, index=False)
```

5. Connect to the OpenAI resource which we created earlier

```python
from langchain_openai import AzureOpenAI

llm = AzureOpenAI(
    deployment_name="gpt-35-turbo-instruct",
    openai_api_type="azure",
    openai_api_key="<<your openAPI key>>",
    azure_endpoint="<<your openAI resource end point>>",
    api_version="<<gather this from the foundry>>"
)
```

6. Create the CSV agent using Langchain and combine the same to a single file and save locally to get the results faster

```python
%pip install langchain_experimental
from langchain_experimental.agents import create_csv_agent

agent = create_csv_agent(
    llm=llm, 
    path='combined.csv', 
    verbose=True, 
    low_memory=False, 
    allow_dangerous_code=True
)
```

7. Invoke the agent and ask the questions which are structured queries but in human-readable format

```python
agent.invoke("how many addresses are from Texas?")
```

8. Invoke the agent and ask more complicated questions which are structured queries but in human-readable format which also did not gave us the right answers in the past milestones

```python
agent.invoke("can you list down all the address IDs for the addresses from Texas?")
```

Congratulations! 🎉 You are now able to talk to the CSV using the OpenAI resources programmatically. The last two questions weren't answered in the first 3 milestones, and we started getting the correct responses for the questions we asked in the format we want! 🏆

These 4 milestones represent the journey of GenAI apps over the last 24-36 months. 🕰️ At this point, we can converse with any type of data using OpenAI ML frameworks and Foundry offerings. 💬

### Milestone #4: Result ✨

The output will be more accurate, giving you answers just like how you query structured data, but without having to remember any syntax and can be done in human-readable prompts. 🤩 The next step is to use different frameworks and create different agents to achieve specific goals for your organization. 🎯 It can be multi-agent, single agent using different frameworks, different sources of data, and then deploy all this as a web app or simple websites (which use Azure web apps) or using Python programming (there are lightweight packages to deploy this as websites). 🌐

Now we have solved all the use cases of reading different source files and getting responses based on the source data. 🥳 At this point, the intelligence of the app is the same as that of the intelligence of the prompt engineer who is asking the question. How can you make that also better? Enter multi-agent applications! 🧠 These are small, separate autonomous systems that will talk in parallel, serial, or in back-and-forth conversations, giving you a final reformed product that otherwise would take hours to find out. 🚀
Learn more about multi-agent AI applications in the coming challenge! 📚

Congratulations once again!!!! 👏

### Extra Credits 🌟

- Deploy your web app using the new deployment you just finished and test it. 🚀
- Understand the difference between Temperature and P value, play around with them and see how the results vary. 🌡️
- Change the model instruction and context, in a funny way or in a tone used by your favorite movie character. 🎭
- Check out more details on how Fabric can be used as a source for the AI app, when it will be in preview, and when it will be GA. 🧵

### Clean Up 🧹

You can remove the deployments one by one and once done, get rid of the resource group you created, and that should clean up everything. 🗑️ Do it the next day after the lab so that you can revisit in case of any doubts for a good 12 hours. ⏳