import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiohttp import web
from routes.transactions import fin_router

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL') 
WEBHOOK_PATH = "/webhook"  

# Bot and dispatcher initialization
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Router registration
dp.include_router(fin_router)

# Create web application
app = web.Application()

# webhook setup
async def on_startup(app):
    await bot.set_webhook(url=f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    logging.info(f"Webhook: {WEBHOOK_URL}{WEBHOOK_PATH}")

# Close webhook on shutdown
async def on_shutdown(app):
    await bot.delete_webhook()
    logging.info("Webhook delted")

# Registration of hooks
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Webhook handler setup
webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)

# Path setup
webhook_handler.register(app, path=WEBHOOK_PATH)

# aiogram integration
setup_application(app, dp, bot=bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, host="0.0.0.0", port=8080)