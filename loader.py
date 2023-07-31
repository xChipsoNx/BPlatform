from aiogram import Bot, Dispatcher
from utils import bank_db
from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage(),fsm_strategy=FSMStrategy.CHAT)
#db_bot = DatabaseManager('data/storage_db/bot_db.db')
db_bank = bank_db.DatabaseManagerBank('data/storage_db/banking_db.db')