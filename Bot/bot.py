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

# Use environment variables for Key Vault access
KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME", "FishingBot")
credential = DefaultAzureCredential()
vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)

# Retrieve secrets from Key Vault
try:
    CQA_API_KEY = client.get_secret("CQA-API-KEY").value
    OPENAI_API_KEY = client.get_secret("OPENAI-API-KEY").value
    # Add more secrets if needed
except Exception as e:
    logger.error(f"Error retrieving secrets from Key Vault: {e}")
    raise

def handle_message(user_message):
    """Process the user message and return a simple response."""
    logger.info(f"Processing message: {user_message}")
    return "Hello! This is a test response."
