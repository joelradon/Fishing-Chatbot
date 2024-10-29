import azure.functions as func
import logging
import json
from Bot import bot  # Import the entire bot module

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Azure Function triggered by Telegram webhook.")

    try:
        # Parse JSON request
        request_body = req.get_body().decode('utf-8')
        logger.info(f"Request body: {request_body}")
        update = json.loads(request_body)
        
        if 'message' in update:
            # Forward the message to the bot's handle_message function
            await bot.handle_update(update)
            return func.HttpResponse("Processed by bot", status_code=200)
        else:
            logger.warning("No message in request.")
            return func.HttpResponse("Invalid request: no 'message' field", status_code=400)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return func.HttpResponse("Error processing request", status_code=500)
