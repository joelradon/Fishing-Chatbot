# Fishing Bot Telegram Integration

## Overview
This bot is designed to provide helpful information about fishing by integrating with Azure's Custom Question Answering (CQA) and OpenAI's GPT-4 model. It runs on Telegram and can answer a wide variety of fishing-related questions.

The bot leverages two main services:

1. **Custom Question Answering (CQA)** - Trained with fishing-specific content to provide direct answers to frequently asked questions.
2. **OpenAI GPT-4** - Used to provide more general answers if CQA doesn't have a sufficient response.

## Features
- Integrates with Azure Key Vault to securely manage sensitive tokens and keys.
- Responds to questions in private or group chats on Telegram when specifically tagged or replied to.
- Uses Custom Question Answering to provide focused, knowledge-based answers.
- Uses OpenAI GPT-4 to answer more general questions.
- Supports updating the CQA knowledge base via new question-answer pairs.
- Handles Telegram's message character limits by splitting long answers into multiple messages.

## Setup Instructions

### 1. Azure Key Vault Setup
The bot retrieves its keys and tokens from an Azure Key Vault instance. The following secrets should be added to your Key Vault:
- `TELEGRAM-API-TOKEN`: Telegram bot token.
- `CQA-ENDPOINT`: Endpoint URL for the Custom Question Answering resource.
- `CQA-API-KEY`: API key for the Custom Question Answering service.
- `OPENAI-ENDPOINT`: Endpoint URL for the OpenAI resource.
- `OPENAI-API-KEY`: API key for accessing OpenAI services.

### 2. Running the Bot
Make sure you have the required Python packages installed. You can install them using:

```bash
pip install requests python-telegram-bot azure-identity azure-keyvault-secrets nest_asyncio
```

Run the bot script using:

```bash
python bot.py
```

The bot will run until manually stopped and respond to commands and messages on Telegram.

### 3. Adding the Bot to a Telegram Group
To use the bot in a group:
- Add the bot to your Telegram group.
- Give the bot appropriate permissions to read and send messages.
- You can interact with the bot by mentioning it (`@YourBotName`) in your messages or replying directly to one of its messages.

## Querying the Bot
Once the bot is running, you can interact with it in private or group chats by typing your question and tagging the bot. Examples include:
- "@YourBotName What size rod should I use for euro nymphing?"
- "@YourBotName What is the best bait for redfish?"

The bot will first attempt to answer using the CQA service. If it doesn't find a relevant answer, it will fall back to OpenAI's GPT-4 model.

If the response exceeds the Telegram character limit, the bot will automatically split the response into multiple messages.

## Training the Bot
You can add new entries to the CQA knowledge base through the bot:

### 1. Update Knowledgebase Command
To train the bot, you can send a command like:

```bash
/update_kb "What is fly fishing?" "Fly fishing is an angling method that uses a light-weight lure called an artificial fly."
```

The bot will add this entry to the knowledge base, making it available for future queries.

### 2. Updating Knowledgebase via Code
You can also update the knowledgebase by modifying the bot script directly:
- Use the `update_cqa_knowledgebase` function to add new question-answer pairs.
- Example:

```python
qna_pairs = [
    {"question": "What is euro nymphing?", "answer": "Euro nymphing is a short-line nymphing method that uses thin leaders and weighted flies."}
]
update_cqa_knowledgebase(qna_pairs)
```
This function will update the knowledge base by making a PATCH request to the CQA endpoint.

## Cost-Effective Azure Hosting
The bot can be hosted cost-effectively on Azure using the following services:
- **Azure Functions**: Deploy the Python script as an Azure Function to handle requests in a serverless environment.
- **Azure Container Instances (ACI)**: Use ACI to run the bot in a container. This approach gives more control over dependencies and environment configurations.
- **Azure Virtual Machines**: Deploy on a small Azure VM if more flexibility and control are needed.

Azure Functions are recommended for cost efficiency and scalability if the bot doesn’t need to be online 24/7.

