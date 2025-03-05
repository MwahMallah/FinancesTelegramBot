import asyncio
import logging

from aiogram import Bot, Dispatcher
from routes.transactions import fin_router

import os
from dotenv import load_dotenv

from flask import Flask

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

async def run_flask():
    """Запускает Flask в фоновом потоке"""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, app.run, "0.0.0.0", 8080)

async def main():
    # load token env variable for bot
    load_dotenv()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    #includes finance router and starts polling    
    dp.include_router(fin_router)

    # Create socket task
    socket_task = asyncio.create_task(run_flask())

    # Create bot in separate task
    bot_task = asyncio.create_task(dp.start_polling(bot))
    
    await asyncio.gather(socket_task, bot_task)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())