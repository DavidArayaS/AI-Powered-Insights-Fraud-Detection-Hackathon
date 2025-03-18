# 🏆  Multi-Agent Application

This project demonstrates a multi-agent application that processes data from Azure Blob Storage using LangChain and OpenAI's GPT-3.5 Turbo model. The application consists of two agents:
1. `Agent1`: Queries the data source for entries with `ApprovalStatus` as `Approved`.
2. `Agent2`: Takes the output from `Agent1` and finds the list of users whose credit scores are less than 500.

## 🚀 Requirements

- Python 3.8+
- Azure account with access to Azure Blob Storage
- OpenAI API key

## 🚀 Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/multi-agent-app.git
    cd multi-agent-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use the command `.\venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## 🚀 Configuration

1. Update the Azure Blob Storage connection string and container name in `src/main.py`:
    ```python
    connection_string = "your_connection_string"
    container_name = "your_container_name"
    ```

2. Update the OpenAI API key and other parameters in `src/main.py`:
    ```python
    llm = AzureOpenAI(
        deployment_name="gpt-35-turbo-instruct",
        openai_api_type="azure",
        openai_api_key="your_openai_api_key",
        azure_endpoint="https://your_azure_endpoint",
        api_version="2024-10-21"
    )
    ```

## 🚀 Usage

1. Run the main script:
    ```sh
    python src/main.py
    ```

2. The script will:
    - Download and combine CSV files from Azure Blob Storage.
    - Initialize the LangChain OpenAI model.
    - Create a CSV agent.
    - Use `Agent1` to query approved entries.
    - Use `Agent2` to find users with credit scores less than 500 from the approved entries.

3. The output will be printed to the console.

## 🚀 Project Structure

```
multi-agent-app
├── src
│   ├── agents
│   │   ├── agent1.py
│   │   ├── agent2.py
│   │   └── __init__.py
│   ├── data_source.py
│   ├── main.py
│   └── utils
│       └── helpers.py
├── requirements.txt
└── README.md
```
