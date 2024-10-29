import azure.functions as func
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Minimal Azure Function entry point to confirm Azure Function connectivity.
    """
    logging.info("Received a request at the minimal Azure Function.")
    return func.HttpResponse("Minimal Function executed successfully.", status_code=200)
