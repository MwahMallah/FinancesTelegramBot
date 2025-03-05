from aiogram import F, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from fsm.transaction import TransactionContext

from util import category_menu_markup, new_transaction_markup, process_category_markup, remove_chat_buttons

fin_router = Router()

@fin_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Выберите действие', reply_markup=new_transaction_markup())

@fin_router.message(F.text == 'Новая транзакция')
async def new_transaction(message: Message, state: FSMContext):
    # Remove the markup when starting the transaction process
    await remove_chat_buttons(message)

    await message.answer('Введите категорию', reply_markup=category_menu_markup())
    await state.set_state(TransactionContext.category)

@fin_router.callback_query(F.data.startswith("category:"), TransactionContext.category)
async def process_category_selection(callback: types.CallbackQuery, state: FSMContext):
    # Extract selected category
    category = callback.data.split(":")[1]
    
    # Update state with selected category
    await state.update_data(category=category)
    
    # Edit the message to show selected category with confirmation options
    await callback.message.edit_text(
        f"Выбрана категория: {category}\n\n"
        f"Подтверждаете выбор или хотите выбрать другую категорию?", 
        reply_markup=process_category_markup()
    )

@fin_router.callback_query(F.data == "confirm_category", TransactionContext.category)
async def confirm_category(callback: types.CallbackQuery, state: FSMContext):
    # Get current data
    current_data = await state.get_data()
    category = current_data.get('category')
    
    # Edit message to proceed to description
    await callback.message.edit_text(f"Выбрана категория: {category}\n\nТеперь введите описание:")
    
    # Set next state
    await state.set_state(TransactionContext.description)

@fin_router.callback_query(F.data == "change_category", TransactionContext.category)
async def change_category(callback: types.CallbackQuery, state: FSMContext):
    # Rebuild the original category selection keyboard

    # Edit message to show category selection again
    await callback.message.edit_text(
        "Выберите категорию", 
        reply_markup=category_menu_markup()
    )

@fin_router.message(TransactionContext.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    
    # Get the full transaction data
    data = await state.get_data()
    await message.answer(
        f'Описание = {data["description"]}, Категория = {data["category"]}'
    )
    
    # Clear the state and return to the main menu with the original markup
    await state.clear()
    await message.answer('Транзакция сохранена.', reply_markup=new_transaction_markup())