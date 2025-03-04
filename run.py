import asyncio
import logging

from aiogram import Bot, Dispatcher
from routes.finances import fin_router

import os
from dotenv import load_dotenv

async def main():
    # load token env variable for bot
    load_dotenv()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    #includes finance router and starts polling    
    dp.include_router(fin_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())