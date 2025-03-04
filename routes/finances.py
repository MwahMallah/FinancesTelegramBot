from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

fin_router = Router()

@fin_router.message(CommandStart())
async def cmd_start(message: Message):
    return message.answer('Привет мир!')
    
@fin_router.message(Command('help'))
async def cmd_help(message: Message):
    return message.answer('Ввели /help')