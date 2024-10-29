import azure.functions as func
import logging
import json
from Bot.bot import handle_message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Step 1: Received a request to the Azure Function.")

    try:
        # Step 2: Log the raw body content
        request_body = req.get_body().decode('utf-8')
        logger.info(f"Step 2: Raw request body: {request_body}")

        # Step 3: Attempt to parse the JSON
        data = json.loads(request_body)
        logger.info(f"Step 3: Parsed request data: {data}")

        # Step 4: Ensure 'message' exists in the request
        if 'message' in data:
            user_message = data['message'].get('text', '')
            chat_id = data['message']['chat']['id']
            logger.info(f"Step 4: Received message '{user_message}' from chat_id {chat_id}")

            # Step 5: Handle the message and send a response
            response_message = handle_message(user_message)
            logger.info(f"Step 5: Response message: {response_message}")

            send_telegram_message(chat_id, response_message)
            return func.HttpResponse("Message processed successfully", status_code=200)
        else:
            logger.warning("Step 4: No 'message' field found in the JSON request.")
            return func.HttpResponse("No 'message' field in JSON", status_code=400)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        return func.HttpResponse("Invalid JSON format", status_code=400)
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return func.HttpResponse("Error processing request", status_code=500)

def send_telegram_message(chat_id, text):
    import requests
    TELEGRAM_API_TOKEN = "Your-Telegram-API-Token"  # Replace with token or secure retrieval method
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    logger.info(f"Step 6: Telegram API response: {response.text}")
