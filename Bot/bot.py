import os
import requests
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

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
except Exception as e:
    logger.error(f"Error retrieving secrets from Key Vault: {e}")
    raise

def handle_message(user_message):
    """Process the user message and return a simple response for testing."""
    logger.info(f"Processing message: {user_message}")
    # Here you can integrate your CQA or OpenAI logic
    return "Hello! This is a test response."  # Static response for testing

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
        response.raise_for_status()  # Raise an error for bad responses
        logging.info(f"Sent message to Telegram: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message to Telegram: {e}")
