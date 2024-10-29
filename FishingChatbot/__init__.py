import azure.functions as func
import logging
import os
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from Bot.bot import handle_message  # Import the message handling function

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve the Telegram API token from Azure Key Vault
try:
    KEY_VAULT_NAME = os.getenv("KEY_VAULT_NAME", "FishingBot")
    vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    TELEGRAM_API_TOKEN = client.get_secret("TELEGRAM-API-TOKEN").value
    logging.info("Successfully retrieved Telegram API token from Key Vault.")
except Exception as e:
    logging.error(f"Error retrieving secrets from Key Vault: {e}")
    TELEGRAM_API_TOKEN = None  # Handle gracefully if needed

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main Azure Function entry point for processing incoming HTTP requests from Telegram
    and responding with the bot's messages.
    """
    logging.info("Received a request from Telegram")

    if not TELEGRAM_API_TOKEN:
        logging.error("Telegram API token not available. Exiting.")
        return func.HttpResponse("Server error: API token not available", status_code=500)

    # Parse the incoming JSON from the request body
    try:
        request_body = req.get_json()
        logging.info(f"Request body: {request_body}")

        if 'message' in request_body:
            message = request_body['message']
            user_message = message.get('text', '')
            chat_id = message['chat']['id']

            # Log the user message
            logging.info(f"User message received: {user_message}")

            # Get bot's response by calling handle_message from bot.py
            response_message = handle_message(user_message)
            logging.info(f"Response to be sent: {response_message}")

            # Send the response back to the user on Telegram
            send_telegram_message(chat_id, response_message)
            return func.HttpResponse("Message processed successfully", status_code=200)
        else:
            logging.warning("No 'message' field found in the request body.")
            return func.HttpResponse("No message to process", status_code=400)
    except ValueError as ve:
        logging.error(f"JSON parsing error: {ve}")
        return func.HttpResponse("Bad Request: Invalid JSON format", status_code=400)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
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

    try:
        response = requests.post(url, json=data)
        logging.info(f"Sent message to Telegram. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message to Telegram: {e}")
