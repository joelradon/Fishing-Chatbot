import os
import requests
import asyncio
import nest_asyncio
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Apply nest_asyncio to handle nested event loops (important for environments where the loop is already running)
nest_asyncio.apply()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set up Azure Key Vault access
KEY_VAULT_NAME = "FishingBot"
credential = DefaultAzureCredential()
vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)

# Retrieve secrets from Key Vault
try:
    TELEGRAM_API_TOKEN = client.get_secret("TELEGRAM-API-TOKEN").value
    CQA_ENDPOINT = client.get_secret("CQA-ENDPOINT").value
    CQA_API_KEY = client.get_secret("CQA-API-KEY").value
    OPENAI_ENDPOINT = client.get_secret("OPENAI-ENDPOINT").value
    OPENAI_API_KEY = client.get_secret("OPENAI-API-KEY").value
except Exception as e:
    logger.error(f"Error retrieving secrets from Key Vault: {e}")
    raise

# Start function to greet users
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command")
    await update.message.reply_text('Hi! I am your fishing bot. Ask me anything about fishing!')

# Function to handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the bot was mentioned with "@" in a group or if the message is a reply to one of its messages
    mentioned_in_group = update.message.chat.type in ['group', 'supergroup'] and f"@{context.bot.username}" in update.message.text
    is_reply = update.message.reply_to_message is not None

    # Allow the bot to respond if it's a direct message or it was mentioned in a group or replied to its own message
    if update.message.chat.type == 'private' or mentioned_in_group or is_reply:
        user_question = update.message.text
        logger.info(f"Received question: {user_question}")

        # Try to get an answer from CQA first
        cqa_answer = query_cqa(user_question)

        if cqa_answer:
            logger.info("Answer found using Custom Question Answering")
            await update.message.reply_text(cqa_answer)
        else:
            # If CQA doesn't have an answer, fall back to OpenAI
            logger.info("No answer found in Custom Question Answering, falling back to OpenAI")
            openai_answer = query_openai(user_question)
            await update.message.reply_text(openai_answer)

# Function to query Custom Question Answering
def query_cqa(question: str) -> str:
    headers = {
        'Ocp-Apim-Subscription-Key': CQA_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "question": question
    }

    try:
        response = requests.post(CQA_ENDPOINT, headers=headers, json=data)
        logger.info(f"Custom Question Answering API response status: {response.status_code}")
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        answers = response.json().get('answers', [])
        if answers and answers[0]['confidenceScore'] > 0.8:
            return answers[0]['answer']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying Custom Question Answering: {e}")
        if response:
            logger.error(f"Response content: {response.content}")

    return None

# Function to query OpenAI gpt-4o-mini
def query_openai(prompt: str) -> str:
    headers = {
        'api-key': OPENAI_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": 0.7
    }
    # Use the correct target URI for your OpenAI deployment
    response = requests.post(
        f"{OPENAI_ENDPOINT}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get('choices', [{}])[0].get('message', {}).get('content', 'Sorry, I couldn\'t generate a response.')
    else:
        return f"Sorry, I am having trouble reaching the AI service. Error code: {response.status_code}"

# Function to add new entries to the Custom Question Answering knowledgebase
def update_cqa_knowledgebase(qna_pairs: list) -> str:
    headers = {
        'Ocp-Apim-Subscription-Key': CQA_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "add": {
            "qnaPairs": qna_pairs
        }
    }
    try:
        response = requests.patch(CQA_ENDPOINT, headers=headers, json=data)
        logger.info(f"CQA API response status: {response.status_code}")
        response.raise_for_status()
        return "Knowledgebase updated successfully."
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating Custom Question Answering knowledgebase: {e}")
        return f"Error updating knowledgebase: {e}"

# Main function to set up the bot
async def main() -> None:
    # Create the application with the API token
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until manually stopped
    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Unexpected error: {e}")