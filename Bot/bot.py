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
    TELEGRAM_API_TOKEN = client.get_secret("TELEGRAM-API-TOKEN").value
    CQA_ENDPOINT = client.get_secret("CQA-ENDPOINT").value
    CQA_API_KEY = client.get_secret("CQA-API-KEY").value
    OPENAI_ENDPOINT = client.get_secret("OPENAI-ENDPOINT").value
    OPENAI_API_KEY = client.get_secret("OPENAI-API-KEY").value
except Exception as e:
    logger.error(f"Error retrieving secrets from Key Vault: {e}")
    raise

def handle_message(user_message):
    """Process the user message and return a simple response for testing."""
    logger.info(f"Processing message: {user_message}")
    return "Hello! This is a test response."

def query_cqa(question: str) -> str:
    """Query the Custom Question Answering service."""
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

    return None

def query_openai(prompt: str) -> str:
    """Query the OpenAI API."""
    headers = {
        'api-key': OPENAI_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": 0.7
    }
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
