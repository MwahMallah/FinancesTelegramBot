from aiogram.fsm.state import StatesGroup, State

class TransactionContext(StatesGroup):
    description = State()
    category = State()