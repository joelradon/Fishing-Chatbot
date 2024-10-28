import azure.functions as func
import logging
import os
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from Bot.bot import handle_message  # Import your message handling function

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Use environment variables for Key Vault access
KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME", "FishingBot")
credential = DefaultAzureCredential()
vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)

# Retrieve secrets from Key Vault
try:
    TELEGRAM_API_TOKEN = client.get_secret("TELEGRAM-API-TOKEN").value
except Exception as e:
    logging.error(f"Error retrieving secrets from Key Vault: {e}")
    raise


# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route(route="FishingChatBotTelegram")
def FishingChatBotTelegram(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received a request from Telegram.')

    # Log the entire request body
    try:
        request_body = req.get_body().decode('utf-8')
        logging.info(f"Request body: {request_body}")  # Log the entire request body
        
        # Check if we have a valid JSON body
        update = req.get_json()
        logging.info(f"Parsed update: {update}")

        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            user_message = message.get('text', '')
            logging.info(f"User message: {user_message}")

            # Static response for testing
            response_message = "Hello! This is a test response."
            send_telegram_message(chat_id, response_message)
            logging.info(f"Sent response: {response_message}")
        else:
            logging.warning("No message found in the update.")
        
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Error processing request.", status_code=400)

    return func.HttpResponse("Webhook received successfully!", status_code=200)

def send_telegram_message(chat_id, text):
    # Send a message back to the user on Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    logging.info(f"Sent message to Telegram: {response.text}")
