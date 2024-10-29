import azure.functions as func
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Received a request.")

    # Log the raw body content for debugging
    try:
        request_body = req.get_body().decode('utf-8')
        logger.info(f"Raw request body: {request_body}")

        # Parse the JSON body
        data = json.loads(request_body)
        logger.info(f"Parsed request data: {data}")

        # Check for 'message' field
        if 'message' in data:
            user_message = data['message'].get('text', '')
            chat_id = data['message']['chat']['id']
            logger.info(f"Received message: {user_message} from chat_id: {chat_id}")

            # Send back a simple response message
            response_message = f"Echo: {user_message}"
            send_telegram_message(chat_id, response_message)
            return func.HttpResponse("Message processed successfully", status_code=200)

        logger.warning("No 'message' field in request.")
        return func.HttpResponse("No 'message' found", status_code=400)

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return func.HttpResponse("Error processing request", status_code=500)

def send_telegram_message(chat_id, text):
    import requests
    TELEGRAM_API_TOKEN = "Your-Telegram-API-Token"  # Replace this with Key Vault retrieval
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    logger.info(f"Telegram response: {response.text}")
