import os
import logging
import requests
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Setup
nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

# Credentials (use Key Vault retrieval here if needed)
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Initialize bot
application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! I am your fishing bot. Ask me anything about fishing!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# New function to handle incoming JSON updates from `__init__.py`
async def handle_update(update_json):
    update = Update.de_json(update_json, application.bot)
    await application.initialize()  # Initialize the bot if necessary
    await handle_message(update, None)

# Set up command and message handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
