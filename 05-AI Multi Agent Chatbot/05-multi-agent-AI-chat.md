# 🏆 Solution Guide 5: AI Solution Accelerators

## 📖 Understanding the Concepts  

Contoso now has a functional basic chatbot, and pilot users are already seeing value from being able to access and query data. 
Definitely, adding Agentic Reasoning capabilities to **Contoso BOT** brings value for the organization in key aspects like:

- Increase efficency with Parallel Problem Solving capabilities. 
- Improve Accuracy with Multi-Perspective Analysis.
- Provide a personalize and more enhanced user experience.

Since the acceptance has been so possitive, the Data team now has the task of improving the capabilities from **Contoso BOT** and get it ready for Production in the following weeks.  
However, before we further develop on our Dev Environment, we need to understand some key concepts. 

### AI Agent Abstractions
----

![Architecture](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/acba652f3b97b9498ae280ea727e1011c5fbacad/05-AI%20Multi%20Agent%20Chatbot/Reference%20Pictures/Image1.png)


### Multi Agent Logical Architecture
----

![Architecture](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/acba652f3b97b9498ae280ea727e1011c5fbacad/05-AI%20Multi%20Agent%20Chatbot/Reference%20Pictures/Image3.png)


### Agents orchestration and communication styles
----

![Architecture](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/0817d840d6d42479f012a4a9667743931cb4de5f/05-AI%20Multi%20Agent%20Chatbot/Reference%20Pictures/Image3.png)


### Azure Agent Frameworks
----

💡 **Semantic Kernel**

- Semantic Kernel is a lightweight, open-source development kit ( SDK ) that lets you easily build AI agents and integrate the latest AI models into your C#, Python, or Java codebase. It serves as an efficient middleware that enables rapid delivery of enterprise-grade solutions.
- In our previous challenge we leverage ** LangChain ** which is an opensource Framework to demostrate ease of integration. 

💡 **AutoGen**

- AutoGen is an open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks. AutoGen aims to provide an easy-to-use and flexible framework for accelerating development and research on agentic AI.

💡 **Langgraph**

- It is an specialized library within the LangChain ecosystem specifically designed for building statefull multi-agent systems. 


----

Now that we have a clear scope of Services, Frameworks and Tools to leverage, lets talk about what a Solution Accelerator is:

----

🚀 Understanding Azure Solution Accelerators
----
Solution accelerators are pre-built, open-source solutions designed to accelerate proof of value. 
They provide a starting point for the most common scenarios and are adaptable to partners' and customers' business needs.

If we translate this to our scenario, we can quickly deploy a full proof of concept with all capabilities we have built so far, this serves many porpuses:

- We can deploy them in isolated Resource groups for rapid testing of new solution capabilities.
- Understanding AI Deployment best practices, same as coding structures that your Dev Teams can leverage.
- Quickly deliver Proof of concepts and even minimal viable produts. 

Lets see it in action, we will leverage a sample Github repository that deploys a complete use case, but we will make some changes on the code so the action it performs is aligned to our business.
 
### Sample Solution Accelerator Architecture
----
![Architecture](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/acba652f3b97b9498ae280ea727e1011c5fbacad/05-AI%20Multi%20Agent%20Chatbot/Reference%20Pictures/simple-architecture-diagram.png)


## Learning Objectives 
----
- Grounding with Bing Search
- Semantic similarity search
- Prompty

## Deployment Guide for Solution Accelerator
----
First action is to open the repository using GitHub Codespace

### Open the Source Code Github Repository 
 
- Open the [Contoso Creative Writer](https://github.com/Azure-Samples/contoso-creative-writer) Github Repository
- Click on the Code Button, and then select the CodeSpaces tab
- On the first option, click on the + sign to create a new Codespace based on the Main Branch

### Customizing the Deployment
----
Within the Codespaces, we will perform a series of changes on the Files so we adapt it to our current Financial use case. 

- Changing the Products CSV File
- Expand the Data file, and click on products.csv
- Agents Prompty Configuration on src/api/agents/
- Editor.prompty, Product.prompty, Researcher.prompty


### Deploy on GitHub Codespaces

Open in GitHub Codespaces

Open a terminal window.

Sign in to your Azure account. You'll need to login to both the Azure Developer CLI and Azure CLI:

1. First with Azure Developer CLI

```
azd auth login
```


2. Then sign in with Azure CLI

```
az login --use-device-code
```
3. Provision the resources and deploy the code:

```
azd up
```





## References


- [Grounding with Bing Search](https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/bing-grounding?view=azure-python-preview&tabs=python&pivots=overview) 
- [Prompty for OpenAI](https://prompty.ai/) 
- [Solution Accelerator on GitHub](https://github.com/Microsoft/solution-accelerators) 
- [LLM based development tools: LangChain vs Semantic Kernel](https://techcommunity.microsoft.com/blog/educatordeveloperblog/llm-based-development-tools-promptflow-vs-langchain-vs-semantic-kernel/4149252) 
- [Autogen Github](https://github.com/microsoft/autogen)



