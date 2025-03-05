import asyncio
import logging

from aiogram import Bot, Dispatcher
from routes.transactions import fin_router

import os
from dotenv import load_dotenv

async def main():
    # load token env variable for bot
    load_dotenv()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    #includes finance router and starts polling    
    dp.include_router(fin_router)
    # Создаём event loop
    loop = asyncio.get_running_loop()
    
    # Ожидаем запуск бота в отдельной задаче
    task = loop.create_task(dp.start_polling(bot))
    await task

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())