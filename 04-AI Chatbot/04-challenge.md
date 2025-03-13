# 🏆 Challenge 04: Setting Up LLMs for a Chatbot and its Dependencies

## 📖 Learning Objectives
Retrieval Augmented Generation (RAG) is a technique used to **build chat-based applications** that leverage custom data to generate more **factual, relevant** responses. Instead of relying solely on a model’s pre-training, RAG retrieves **grounding data** from your own data store (for example, Azure AI Search) and **augments** the prompt with that data. In this challenge, you’ll use **Azure AI Foundry** to orchestrate these steps.

By completing this challenge, you'll be able to:

- **Identify** the need to ground your language model with RAG  
- **Index** your data with **Azure AI Search** to make it searchable for language models  
- **Build** an AI agent on your own data in the **Azure AI Foundry portal**  
- **Create** a **prompt flow** to maintain **chat history**  
- **Retain** conversation context so the chatbot can respond accordingly in multi-round conversations  

---

## ⚙️ Prerequisites
Before starting, ensure you have:

- **Familiarity** with fundamental AI/ML concepts in Azure.  
- **Permissions** to create an Azure AI Foundry hub (or have one created for you).  
- **Azure roles**: If your role is **Contributor** or **Owner**, you can follow these steps. If your role is **Azure AI Developer**, the hub must already be created, and your user role must be **Azure AI Developer, Contributor, or Owner** on that hub.

[Check this for more information](https://microsoft.github.io/AI-For-Beginners/)

---

## 🏆 Challenge Overview

### Milestone #1: **Create, Define, and Explore** LLMs + Resources
1. **Create** your Resource Group, Key Vault, Azure Storage, Azure AI Service, and Azure AI Search.
2. **Set up** an AI Foundry **Hub** and **Project**.
3. **Deploy** two models: an **embedding** model (e.g., `text-embedding-ada-002`) and a **chat** model (e.g., `gpt-35-turbo-16k`).
4. **Test** your chatbot in the **playground** with simple questions.

### Milestone #2: **Add Data** to Your Project and **Ground** the Chatbot
1. **Enable Managed Identity** and **assign roles** for your AI service, AI Search, and storage.
2. **Create** connections in the AI Foundry (ml.azure.com or ai.azure.com).
3. **Index** your data with **Azure AI Search**.
4. **Attach** that index to your chat model so it uses your **custom data** to respond.

### Milestone #3: **Build & Customize** – Prompt Flow with Orchestration
1. **Clone** the “Multi-Round Q&A on Your Data” sample.
2. **Incorporate** your vector index to retrieve relevant info.
3. **Deploy** a **prompt flow** endpoint that retains chat history.
4. **Test** multi-turn Q&A that references your data.

### Milestone #4: **Advanced** – Query Multiple CSV Files with Langchain + Azure OpenAI
1. **Create** or verify your **Azure OpenAI** resource for `gpt-35-turbo-instruct`.
2. **Combine** multiple CSVs into one local CSV (or manage them individually).
3. **Use** `create_csv_agent` in Python to ask structured queries in plain English.
4. **Achieve** more complex or SQL-like queries without memorizing syntax.

---

## 💡 Key Definitions

- **Playground**: A low-code environment in Azure AI Foundry for experimenting with models.
- **Azure AI Services**: A collection of AI offerings (like Cognitive Services, Azure OpenAI, etc.).
- **Prompt flow**: A pipeline or workflow in Azure ML or AI Foundry that orchestrates how input, retrieval, augmentation, and model inference are chained together.
- **Grounding**: Providing the LLM with factual, relevant data to reduce hallucinations and improve context accuracy.
- **Retrieval Augmented Generation (RAG)**: A pattern where data is retrieved from an index or database, then appended to the user’s query before calling the LLM.
- **Azure AI Search**: A service to index and retrieve your data (supports vector-based, semantic, keyword, or hybrid search).
- **Agent**: In Foundry, an AI agent can automatically retrieve data, interact with knowledge sources, and produce answers or even execute actions.

---

## Why We Need RAG

When you ask an LLM a question, it normally only relies on **static training data**. If that data is outdated or missing details about your **specific** documents, the model might respond with **“hallucinated”** info.

**RAG** addresses this by:
1. Retrieving relevant context from an **external** data source (like your CSV or text files).
2. **Augmenting** the prompt with that context so the model uses fresh, correct info.
3. **Generating** a more **accurate** and **domain-specific** answer.

---

## How RAG Works in Azure AI Foundry

1. **Upload and index** your data in Azure AI Search.
2. **Enable** a vector-based or hybrid search index.
3. **Create** or configure a prompt flow (multi-round chat, single question, or an agent approach).
4. The flow:
   1. Takes the user query (“How many clients do we have in Wayne Enterprises?”).
   2. **Retrieves** relevant docs from your index (like partial CSV data).
   3. **Concatenates** that data to the query.
   4. **Calls** the LLM with the augmented prompt.
   5. **Produces** an answer referencing your data.

---

## 🧭 Step-by-Step Challenge

### 1. **Set Up the Basic Resources** (Milestone #1)
- **Resource Group** in Azure
- **Azure Storage** with a container `refined-data` (upload your CSVs or TXTs)
- **Azure AI Service** (Standard tier for `gpt-35-turbo` or `gpt-35-turbo-instruct`)
- **Azure AI Search** (Standard tier, possibly with increased replicas/partitions if you have heavier data)
- **Key Vault** (standard tier recommended)
- **AI Foundry**: Create **Hub** → then **Project**.

### 2. **Deploy Your Models** in the Foundry
- For instance, `text-embedding-ada-002` for embeddings and `gpt-35-turbo-16k` for chat.

### 3. **Connect and Index** (Milestone #2)
- Assign roles/IAM so your AI service and search can read from your storage.
- Create a **connection** to `refined-data` container in Foundry.
- **Index** your CSV or TXT data in Azure AI Search.
- **Add** that index to your chat model in the Playground.

### 4. **Prompt Flow** (Milestone #3)
- **Clone** “Multi-Round Q&A on Your Data”.
- Adjust the **lookup node** to use your vector index ID.
- Save and test. Deploy the flow if needed to create an endpoint.

### 5. **Langchain + Azure OpenAI** (Milestone #4)
- If you want more advanced queries (like “List all address IDs from Texas, grouped by city”), consider writing a Python script:
  - `create_csv_agent(llm, path='combined.csv')`
  - `agent.invoke("SQL-style question here...")`
- This approach is ideal if you want minimal user friction for structured queries.

---

## ⚙️ Extra Hints & Goodies

## 🧑‍💻 Python Code Implementation

## Install Required Dependencies
```python
%pip install openai
%pip install langchain
%pip install pandas
%pip install langchain_experimental
%pip install langchain_openai
%pip install tabulate
%pip install azure-storage-blob
```
##Load and Combine CSV Files from Azure Storage

```python

import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient

# Azure Storage Connection
connection_string = "<<YOUR_STORAGE_CONNECTION_STRING>>"
container_name = "refined-data"
blob_names = ["DimAddress.csv", "DimApplicant.csv", "DimClient.csv", "factfinancial.csv"]

# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Download and combine CSVs
dataframes = []
for blob_name in blob_names:
    blob_client = container_client.get_blob_client(blob_name)
    blob_content = blob_client.download_blob().content_as_text()
    
    # Convert CSV content to Pandas DataFrame
    df = pd.read_csv(StringIO(blob_content))
    dataframes.append(df)

# Merge all DataFrames
combined_df = pd.concat(dataframes, ignore_index=True)

# Save locally
combined_csv_path = "combined.csv"
combined_df.to_csv(combined_csv_path, index=False)
```
##Connect to Azure OpenAI and Deploy LLM

```python
from langchain_openai import AzureOpenAI

# Define OpenAI Connection
llm = AzureOpenAI(
    deployment_name="gpt-35-turbo-instruct",
    openai_api_type="azure",
    openai_api_key="<<YOUR_OPENAI_API_KEY>>",
    azure_endpoint="<<YOUR_AZURE_OPENAI_ENDPOINT>>",
    api_version="<<YOUR_AZURE_OPENAI_API_VERSION>>"
)
```

##Create Langchain CSV Agent

```python
%pip install langchain_experimental
from langchain_experimental.agents import create_csv_agent

# Create Langchain CSV Agent
agent = create_csv_agent(
    llm=llm, 
    path='combined.csv', 
    verbose=True, 
    low_memory=False, 
    allow_dangerous_code=True
)
```
##Query the Data Using Natural Language

```python
# Simple Query: Count Addresses from Texas
agent.invoke("How many addresses are from Texas?")
```
```python
# Complex Query: List All Address IDs from Texas
agent.invoke("Can you list all the address IDs for the addresses from Texas?")
```


**Happy building and hacking!** 🚀

---

## 🏁 Final Checkpoints

1. **Chatbot** references your data: “What’s the ApplicationID of CLI-19708?” and it gives an actual ID from your CSV.  
2. **Prompt flow** can handle multi-round contexts: “What did we just talk about?”  
3. **Langchain** CSV queries produce correct structured answers (like a small SQL aggregator).  
4. **Index** is updated or re-built if you add more data.  

Once done, you have a fully functional **RAG** solution, bridging your data with a powerful LLM. 🎉 

Now you have a **structured challenge guide** with **Python scripts** embedded, making it **fully self-contained**! 🚀🔥

