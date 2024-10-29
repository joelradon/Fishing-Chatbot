import azure.functions as func
import logging
from Bot.bot import handle_message  # Import your message handling function

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Received a request from Telegram")

    # Parse the incoming JSON from the request body
    try:
        request_body = req.get_json()
        logging.info(f"Request body: {request_body}")

        if 'message' in request_body:
            message = request_body['message']
            user_message = message.get('text', '')
            chat_id = message['chat']['id']

            # Call your bot's response function
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
    # Replace this with actual retrieval of your TELEGRAM_API_TOKEN
    TELEGRAM_API_TOKEN = "YOUR_TELEGRAM_API_TOKEN"
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    logging.info(f"Sent message to Telegram: {response.text}")
