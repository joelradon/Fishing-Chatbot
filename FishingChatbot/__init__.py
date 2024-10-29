import azure.functions as func
import logging

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Request received at Azure Function.")
    
    # Try parsing incoming request body for a 'text' field
    try:
        req_body = req.get_json()
        logging.info(f"Request body: {req_body}")
        
        if "message" in req_body and "text" in req_body["message"]:
            user_message = req_body["message"]["text"]
            return func.HttpResponse(f"Message received: {user_message}", status_code=200)
        else:
            return func.HttpResponse("Message field not found in request body", status_code=400)
    except Exception as e:
        logging.error(f"Error parsing request: {e}")
        return func.HttpResponse("Error processing request", status_code=500)
