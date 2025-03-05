import asyncio
import logging

from aiogram import Bot, Dispatcher
from routes.transactions import fin_router

import os
from dotenv import load_dotenv

from util import keep_socket_open

async def main():
    # load token env variable for bot
    load_dotenv()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    #includes finance router and starts polling    
    dp.include_router(fin_router)

    # Create socket task
    socket_task = asyncio.create_task(keep_socket_open())

    # Create bot in separate task
    bot_task = asyncio.create_task(dp.start_polling(bot))
    
    await asyncio.gather(socket_task, bot_task)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())