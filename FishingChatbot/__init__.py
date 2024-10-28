import azure.functions as func
import logging
import json
import os
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from Bot.bot import handle_message  # Import your message handling function

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Azure Key Vault access
KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME", "FishingBot")
credential = DefaultAzureCredential()
vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)

# Retrieve the Telegram API token from Key Vault
try:
    TELEGRAM_API_TOKEN = client.get_secret("TELEGRAM-API-TOKEN").value
except Exception as e:
    logger.error(f"Error retrieving TELEGRAM-API-TOKEN from Key Vault: {e}")
    TELEGRAM_API_TOKEN = None

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main Azure Function entry point for processing incoming HTTP requests
    from Telegram and responding with the bot's messages.
    """
    logging.info("Received a request from Telegram")

    # Check if the Telegram API token was retrieved successfully
    if not TELEGRAM_API_TOKEN:
        logger.error("Telegram API token is missing. Cannot process request.")
        return func.HttpResponse("Server error: Telegram API token is missing.", status_code=500)

    # Parse the incoming JSON from the request body
    try:
        request_body = req.get_json()
        logging.info(f"Request body: {request_body}")

        if 'message' in request_body:
            message = request_body['message']
            user_message = message.get('text', '')
            chat_id = message['chat']['id']

            # Get bot's response by calling handle_message from bot.py
            response_message = handle_message(user_message)
            send_telegram_message(chat_id, response_message)
            return func.HttpResponse("Message processed successfully", status_code=200)
        else:
            logging.warning("No 'message' found in the update")
            return func.HttpResponse("No message to process", status_code=400)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Error processing request", status_code=500)

def send_telegram_message(chat_id, text):
    """
    Send a message to a specific Telegram chat.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    logging.info(f"Sent message to Telegram: {response.text}")
