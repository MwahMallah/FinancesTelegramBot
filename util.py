from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import socket
import asyncio

# Define categories
CATEGORIES = [
    "Питание", "Подарки", "Здоровье/медицина/гигиена", 
    "Дом/проживание", "Транспорт", "Личные расходы", 
    "Домашние животные", "Коммунальные услуги", "Путешествия", 
    "Задолженности", "Техника", "Кафе/ресторан/доставка", 
    "Развлечения", "Одежда и обувь", "Связь и интернет", 
    "Хобби/игры", "Спорт", "Образование"
]

def new_transaction_markup():
    # Main menu markup
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Новая транзакция')]
        ], 
        resize_keyboard=True, 
        input_field_placeholder='Добавить новую транзакцию?'
    )

def category_menu_markup():
    # Categories menu markup
    builder = InlineKeyboardBuilder()
    # Arrange categories in a grid-like structure
    for category in CATEGORIES:
        builder.button(
            text=category, 
            callback_data=f"category:{category}"
        )

    # Adjust the keyboard layout 
    builder.adjust(3)  # 3 buttons per row

    return builder.as_markup()

def process_category_markup():
    # Create inline keyboard with additional option
    builder = InlineKeyboardBuilder()
    
    # Original categories from the previous selection
    builder.button(text="✅ Подтвердить категорию", callback_data="confirm_category")
    builder.button(text="🔄 Выбрать другую категорию", callback_data="change_category")

    return builder.as_markup()

def submit_transaction_markup():
    # Create inline keyboard with additional option
    builder = InlineKeyboardBuilder()
    
    # Original categories from the previous selection
    builder.button(text="✅ Подтвердить транзакцию", callback_data="confirm_transaction")
    builder.button(text="❌ Отменить транзакцию", callback_data="decline_transaction")

    return builder.as_markup()

async def remove_chat_buttons(message: Message, 
                              msg_text: str = r"Loading\.\.\.",):
    msg = await message.reply(msg_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="MarkdownV2")
    
    await msg.delete()