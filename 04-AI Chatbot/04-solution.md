# 📖 Solution to Challenge 04: Setting Up LLMs for a Chatbot and its dependencies.

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
- Check the TPM quota for your subscription for the LLMs `text-embedding-ada-002` and `gpt-35-turbo-16k`. If you are already familiar with the same, request a quota addition if the current quota is in the 2-digit range (10k–90k) and increase it to whatever is maximum for each model.

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
Since we are time-bound, we will just use the Dimension Xls (which will be converted to csv/txt here) for the purpose of this challenge. If you were able to successfully finish the first 3 challenges, you already have 3 Dim xls files with you in Fabric Lakehouse and can convert the files to CSV (using a dataflow to transform, then a data copy pipeline to copy from Fabric to the new storage account) and upload them into the storage account we are going to create below.

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

Once the conversion is completed you can use a **Data Factory copy job** to copy from Fabric to the new storage account (please follow the steps in **Challenge 2** to complete this task).  
**Alternatively**, to keep this challenge simpler, you can **manually** do it:

- Get the `.xls` files and **save them locally** in `.txt` or `.csv` format.
- Save them inside a **subfolder**.
- This folder can then be **uploaded** to the **parent container** in our storage account once the storage account creation steps are completed.

**Reason to go with manual upload**:  
Because the Excel sheet from the previous process might have different formatting, it is often best to upload a folder of all the files saved in `.txt` format directly to the storage account container to **save time**. Additionally, `.xls` can be problematic if there are any formatting issues in the columns, which may cause the file to fail recognition.

1. On the **Storage accounts** page, select **Create**.  
2. Fill in the required details.  
3. Enter the following details:
   - **Subscription**:
   - **Resource group**:
   - **Storage account name**:
   - **Region**:
   - **Performance**: Select **Standard**
   - **Redundancy**: **LRS**
   - **Networking**: Enable public access from all networks (to avoid isolated environment-specific issues)
   - Keep everything else default.
4. Select **Review + Create**.  
5. Click **Create**.

![Create Storage Account](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/2.png)

6. Once the storage account is created, create a container `refined-data` and upload all four CSV files into the container (inside a folder named `csv-data` or `txt-data`). By the end of this step, you will have:
   - A **storage account** with a **container** inside,
   - A **subfolder** inside that container,
   - All the files in CSV format within that subfolder.

When it’s done, it will look like this:

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
   - **Pricing tier**: **Standard**
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
   - **Location**: Choose from any region mentioned in the Tips.
   - **Pricing tier**: **Standard**
   - **Scale**: Increase the search unit by 4 to improve query performance.
2. Wait for your Azure AI Search resource deployment to complete.

![Azure AI Search Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/search5.png)


---

### 5️⃣ Create an Azure AI Service
1. On the **home page**, select **+ Create a resource** and search for **Azure AI Services**. Then create a new Azure AI Service resource with the following settings:
   - **Subscription**:
   - **Resource group**:
   - **Region**: Choose from any of the regions mentioned in the Tips.
   - **Name**:
   - **Pricing tier**: **Standard**
   - **Scale**: Increase the search unit by 4 to improve query performance.
2. Wait for your **Azure AI Service** resource deployment to be completed.

![Azure AI Services Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/aiservice6.png)

**Remarks**: At this point, all the resources needed to build a **Hub** and **Project** inside a Hub in **AI Foundry** are completed.

---

### 6️⃣ Create a Hub
1. On the **AI Foundry** page in [https://portal.azure.com], select **+ Create** and choose **Hub**. Then create a new Hub resource with the following settings:
   - **Subscription**:
   - **Resource group**:
   - **Region**: Select from the recommended regions in the Tips.
   - **Name**:
   - **Connect AI Services incl. OpenAI**: Select the AI service you created earlier from the drop-down.
   - **Storage Tab**: Select the storage account created previously.
   - **Key Vault Tab**: Select the key vault you created.
   - **Networking**: Keep the default (**public**).
   - Keep everything else at the default.
   - Click **Create + Review**, then **Create**.
2. Wait for your **Azure AI Hub** resource deployment to finish.

![Hub Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/hub7.png)

---

### 7️⃣ Create a Project
1. On the **AI Foundry** page in [https://portal.azure.com], select **+ Create** and choose **Project**. Then create a new Project resource with the following settings:
   - **Subscription**:
   - **Resource group**:
   - **Region**: Choose from the recommended regions in the Tips.
   - **Name**:
   - **Hub**: Select the Hub you created in the previous step.
   - Leave the rest at default.
   - Click **Create + Review**, then **Create**.
2. Wait for your **Azure AI Project** resource deployment to complete.

![Project Creation](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/project8.png)

**Remarks**: This should take no more than 20 minutes to build. Once finished, move to the **AI Foundry** page at [https://ai.azure.com]. Select the project, and we will do the remaining work inside this environment.

**TIP**: If there are no organizational policies or constraints, you can sign up at [https://ai.azure.com] and create the project directly. When doing so, all other resources are also created. You just need an **AI search service** resource in advance.

---

### 8️⃣ Deploy Models

You need two models to implement your solution:
- **An embedding model** to vectorize text data for efficient indexing and processing.  
- **A model** that can generate natural language responses to questions based on your data.

1. In the **Azure AI Foundry** portal, go to your **project**. In the **navigation pane** on the left, under **My assets**, select **Models + endpoints**.

2. Create a **new deployment** of the `text-embedding-ada-002` model with the following settings by selecting **Customize** in the Deploy model wizard:

   - **Deployment name**: `text-embedding-ada-002`  
   - **Deployment type**: Standard  
   - **Model version**: Select the default version  
   - **AI resource**: Select the resource you created previously  
   - **Tokens per Minute Rate Limit (thousands)**: Slide it to the maximum  
   - **Content filter**: DefaultV2  
   - **Enable dynamic quota**: (optional; depends on your usage)  

   > **Note**: If your current AI resource location doesn’t have sufficient quota for the model you want to deploy, you may be prompted to choose a different location. A new AI resource will be created and connected to your project if needed.

3. **Repeat** these steps to deploy a `gpt-35-turbo-16k` model with the deployment name `gpt-35-turbo-16k`. (You can experiment with the latest GPT models if you wish.)

4. **Select** the `gpt-35-turbo-16k` model and click **Open in playground**.

5. **Test the chatbot** with a question like “What do you do?” and check the response.

6. **Now change** the model instructions and context message to the following:

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

7. Select **Apply changes**.

8. **Test the chatbot** with the question “What do you do?” to see a context-specific response. Notably, if you asked the same question before updating the context, the answer would have been more generic.

---

## 🚀 Milestone #1: Define & Explore
You can test the model by heading to the **playground** and chatting with it. Ask some generic questions, and you’ll get generic answers. At this point, the model is looking for data it was trained on and is **not** grounded with **custom data** yet. We were also able to customize the model instructions and context to provide more specific responses to user questions.

---

## 🚀 Milestone #2: Add Data to Your Project and Explore the Response of the Chatbot Post Indexing and Grounding

1. **Enable Managed Identity**  
   a. Enable **MI** for both **AI service** and **AI search service**.  
   b. In the **Search service** resource (in the Azure portal):
      - From the left pane, under **Settings**, select **Identity**.
      - Switch **Status** to **On**.
      - Select **Save**.  
   c. In the **Azure AI services** resource (in the Azure portal):
      - From the left pane, under **Resource Management**, select **Identity**.
      - Switch **Status** to **On**.
      - Select **Save**.

2. **Set API Access Control for Search**  
   a. In the **Search service** resource (in the Azure portal):
      - From the left pane, under **Settings**, select **Keys**.
      - Under **API Access control**, select **Both**.
      - When prompted, select **Yes** to confirm the change.

3. **Assign Roles**  
   a. The general pattern for assigning role-based access control (RBAC) to any resource is:
      - Navigate to the **Azure portal** for the given resource.
      - From the left pane, select **Access control (IAM)**.
      - Select **+ Add > Add role assignment**.
      - Search for the role you need and select it. Then click **Next**.
      - When assigning a role to yourself:
        - Select **User, group, or service principal**.
        - Select **Select members**.
        - Search for your name and select it.
      - When assigning a role to another resource:
        - Select **Managed identity**.
        - Select **Select members**.
        - Use the dropdown to find the resource type you want to assign (for example, Azure AI services or Search service).
        - Select the resource from the list. (There might only be one.)
      - Continue through the wizard and select **Review + assign** to finalize.

   b. Use these steps to assign roles for the resources you’re configuring in this tutorial:
      - **Search service** in the Azure portal:
        - **Search Index Data Reader** → Azure AI services managed identity
        - **Search Service Contributor** → Azure AI services managed identity
        - **Contributor** → yourself (to find **Contributor**, switch to the **Privileged administrator roles** tab at the top)
      - **Azure AI services** in the Azure portal:
        - **Cognitive Services OpenAI Contributor** → Search service managed identity
        - **Contributor** → yourself (if not already in place)
      - **Azure Blob storage** in the Azure portal:
        - **Storage Blob Data Contributor** → Azure AI services managed identity & Azure AI services managed identity
        - **Contributor** → yourself (if not already in place)

> **TIP**: If you’re using identity-based authentication, **Storage Blob Data Contributor**, **Storage File Privileged Contributor** (inside Storage account resources), and **Cognitive Services OpenAI Contributor** (inside AI services resource) roles must be granted to individual users that need access on the storage account.

4. **Storage Account Datastore Configuration**  
   a. The best practice is to use **Microsoft Entra Authentication**.  
   b. Enable the **Account Key** for the storage account to gather the information for later use (only if #a isn’t an option).

> **TIP**: Other options include creating SAS URLs or using Entra ID authentication. For simplicity, we’re choosing **Entra ID authentication** in the steps below.

### 5. Create Connections to the Blob Storage & AI Search

   a. You can do this several ways, but one straightforward method is to go to the **Management Center** at [ai.azure.com](https://ai.azure.com) or [ml.azure.com](https://ml.azure.com) and create connections under **Connected resources**. Add a new connection.  
   b. Add the **Azure AI Search** as an internal connection.

   c. For loading custom data (if you haven’t uploaded the files/folder directly to AI Foundry), you can establish the connection as per your needs. Since we’re time-bound and want a solution that works for both organizational constraints and typical ID restrictions, we’ll use **Azure Blob storage**:
      1. Click on **+ New connection**.
      2. Select **Blob storage** from the Data sublist.
      3. Select the **subscription ID**, **storage account**, and **blob container** (the parent container).

      **Option 4#a**:
      4. Under **authentication method**, select **Microsoft Entra ID based**.
      5. Provide a connection name and save it.

      **Option 4#b**:
      4. Under **authentication method**, select **Credential based**.
      5. Under **authentication type**, select **Account key**. Paste in the storage account key you copied earlier, name the connection, and save.

![Connection to Blob Storage](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/conn10.png)


---

### 6. Add the Custom Data to AI Foundry

a. Go to your **project** in **Azure AI Foundry**.  
b. Select **Data + Indexes**.  
c. Select **+ New Data**.  
d. From the drop-down, choose the **data source** corresponding to the connection you created in the previous step. If everything is set up correctly, you’ll be able to **Browse to storage path**; if not, you might only see an option to **Enter storage path manually** (this indicates an access or key issue that you'll need to troubleshoot).  
e. Select the **subfolder** inside your main folder and click **Next**.  
f. Give the data a **friendly name** you can recognize.

![Data Addition in AI Foundry](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/data11.png)

g. Once created, ensure the data is **readable** and displays the **number of files** and **total size**. In the preview window, you should see the files you uploaded.

h. Next, create the **Index** for this newly connected custom data:
1. Go to **Indexes**.
2. Click **+ New Index**.
3. Select the **Data Source** (choose **Data** in AI Foundry since we established the connection and created the data).
4. Select the data you created in the previous step.
5. **Index configuration**: Choose your **AI Search** service name, then assign a **vector index name** you prefer. The compute level might be auto-selected; for better performance, consider a higher compute tier.
6. Choose the **AOAI Service** connection that was set up when creating the project.
7. **Create vector index**.
8. You’ll see a status indicating your data ingestion is in progress. This can take a few minutes or more, depending on the data volume and resource limits. Wait until the **status** changes to show your data source and index name instead of “In progress.”

![Creating a Vector Index](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/vector12.png)

> **TIP**: If you’re curious about what’s happening behind the scenes, click on the job details to visit [https://ml.azure.com](https://ml.azure.com). You can see the jobs and steps running for vector indexing. The duration depends on how many documents you have and how your resources are sized.

![Vector Indexing Status](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/7b4a95aa515d6cea3bffc4253b32ac0981bb527a/04-AI%20Chatbot/Reference%20Pictures/vector13.png)

---

### 7. Add Your Custom Data to Your Chat Model

a. In your **project** on **Azure AI Foundry**, select **Playgrounds**, then **try the chat playground**.  
b. Click **Add your data**.  
c. Choose the **project index** you created in the last step.  
d. For **Search type**, leave it as **hybrid**.  
e. No other changes needed; your chatbot is now configured with **custom data**.  
f. After a refresh, give it a moment and then try asking specific questions like:
   - *What is the Address of ADDR-29841?*
   - *What is the ApplicationID of the customer CLI-19708?*
   - *How many clients does Wayne Enterprises company have?*
   - *How many addresses are from Texas?*
   - *Can you list all the address IDs for the addresses from Texas?*

**Congratulations!**  
You have now trained the model with **your own data**, and it’s ready to provide **domain-specific answers**. Notice:

- If you use **txt** format, responses are often better.
- If you use **csv**, you might see **inconsistent** answers.

### **Milestone #4** will help address some of these limitations by leveraging an **AI agent**.

If you’re using csv data as the source, consider uploading data and creating an index with **txt** files to see if results improve.

You might also notice the app retrieves individual details easily but struggles with **bulk responses**. This is a limitation of the current setup—more **frameworks** or **customization** will be needed for broader or more complex queries.
---

## 🚀 Milestone #2: Result

Build & Customize - Generative AI app that uses your own custom data. You can now chat with the model asking the same question as before, and this time it uses information from your data to construct the response. You can expand the references button to see the data that was used.

---

## 🚀 Milestone #3: Build & Customize - Create, Iterate, and Debug Your Orchestration Flows

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

## 🚀 Milestone #4: Query multiple CSV files using Azure OpenAI & Langchain framework

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

8. Invoke the agent and ask more complicated questions which are structured queries but in human-readable format which also did not give us the right answers in the past milestones

```python
agent.invoke("can you list down all the address IDs for the addresses from Texas?")
```

Congratulations! 🎉 You are now able to talk to the CSV using the OpenAI resources programmatically. The last two questions weren't answered in the first 3 milestones, and we started getting the correct responses for the questions we asked in the format we want! 🏆

These 4 milestones represent the journey of GenAI apps over the last 24-36 months. 🕰️ At this point, we can converse with any type of data using OpenAI ML frameworks and Foundry offerings. 💬

## 🚀 Milestone #4: Result ✨

Your results are **significantly more accurate**, enabling you to query semi-structured or unstructured data in **human-readable prompts** without memorizing any syntax. 🤩 Next, you can explore different frameworks and create other **agents** to fulfill various organizational needs. 🎯 These can include multi-agent systems, single agents working across multiple frameworks or data sources, and potentially deploying your solution as a **web app** or simple site (e.g., using Azure Web Apps), or via Python-based lightweight deployment packages. 🌐

Having addressed all the use cases of reading different source files to retrieve domain-specific answers, 🥳 you’ve extended your application’s intelligence to match the expertise of the prompt engineer’s queries. But how do we push it further? **Enter multi-agent applications**! 🧠 These are small, autonomous subsystems that operate in parallel, in series, or back-and-forth to deliver a refined product—work that might otherwise require hours of manual analysis. 🚀  
Stay tuned to learn more about **multi-agent AI applications** in upcoming challenges! 📚

**Congratulations** once again! 👏

---

### Extra Credits 🌟

- **Deploy your web app** using the new deployment. Test it to see how it behaves in a real environment. 🚀  
- Experiment with **Temperature** and **P value** to understand how they influence response creativity and variability. 🌡️  
- **Customize** the model’s context or instructions with a humorous or thematic style—maybe channel your favorite movie character’s voice. 🎭  
- Investigate how **Microsoft Fabric** can act as a data source for your AI app, noting when new features might be in preview or GA. 🧵  

