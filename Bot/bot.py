import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_message(user_message):
    """Echoes back the received message for basic testing."""
    logger.info(f"Echoing message: {user_message}")
    return f"Echo: {user_message}"
