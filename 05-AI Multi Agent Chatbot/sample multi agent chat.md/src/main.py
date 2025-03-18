import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient
from langchain_openai import AzureOpenAI
from langchain_experimental.agents import create_csv_agent
from agents.agent1 import Agent1
from agents.agent2 import Agent2
from data_source import DataSource

# Initialize Azure Blob Storage connection
connection_string = "<<your storage account connection sting>>"
container_name = "refined-data"
blob_names = ["DimAddress.csv", "DimApplicant.csv", "DimClient.csv", "factfinancial.csv"]

# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
dataframes = []
for blob_name in blob_names:
    blob_client = container_client.get_blob_client(blob_name)

    # Download the blob content
    blob_content = blob_client.download_blob().readall().decode('utf-8')

    # Read the content into a pandas DataFrame
    df = pd.read_csv(StringIO(blob_content))
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a CSV file
combined_csv_path = "combined.csv"
combined_df.to_csv(combined_csv_path, index=False)

# Initialize the LLM
llm = AzureOpenAI(
    deployment_name="gpt-35-turbo-instruct",
    openai_api_type="azure",
    openai_api_key="<<your openai API Key>>",
    azure_endpoint="<<your openai Endpoint>>",
    api_version="2024-10-21"
)

# Create the CSV agent
agent = create_csv_agent(llm=llm, path='combined.csv', verbose=True, allow_dangerous_code=True)

# Initialize DataSource, Agent1, and Agent2
data_source = DataSource(combined_df.to_dict(orient='records'))
agent1 = Agent1(data_source)
agent2 = Agent2(data_source)

# Process approval query with Agent1
approval_message, approved_entries = agent1.process_approval_query()
print(approval_message)

# Process credit score query with Agent2
credit_score_message, low_credit_entries = agent2.process_credit_score_query(approved_entries)
print(credit_score_message)