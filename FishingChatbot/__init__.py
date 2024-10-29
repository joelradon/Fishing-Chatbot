import azure.functions as func
import logging
import json
from Bot.bot import handle_message, send_telegram_message  # Import handle_message and send_telegram_message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main Azure Function entry point for processing incoming HTTP requests
    from Telegram and responding with the bot's messages.
    """
    logging.info("Received a request from Telegram")

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
            send_telegram_message(chat_id, response_message)  # Send response message
            return func.HttpResponse("Message processed successfully", status_code=200)
        else:
            logging.warning("No 'message' found in the update")
            return func.HttpResponse("No message to process", status_code=400)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Error processing request", status_code=500)
