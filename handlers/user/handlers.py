from aiogram import F, Router, types
from aiogram.types import Message 
from aiogram.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
#from keyboards.default import main_kb as mm
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from loader import db_bank
from utils.user_cls import User
from keyboards.inline.user_inline import holders_inline_kb, pp_inline_kb, cash_inline_kb
from keyboards.default import main_kb
from states.states import LKstates


router = Router()  # [1]



@router.message(Command("start"))
async def start_handler(msg: Message, state:FSMContext):
   
    await main_kb.start_menu(msg)
    db_bank.new_user(msg.from_user.id)
    await state.clear()
    
    #await msg.answer("Привет! Я банк платформа",reply_markup=keyboard)


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await main_kb.cancel_kb(message, state)


@router.message(Text("Кабинеты"))
async def fis_holders(message: Message, state:FSMContext):
    await message.answer(
        "Выберите действие из списка:", 
        reply_markup=holders_inline_kb.holders_menu()   
    )
    await state.set_state(LKstates.lk_menu)

@router.message(Text("Настройки"))
async def ip_holders(message: Message):
    pass
    """data = db_bank.get_name_holders("'IP'")
    await message.answer(
        "Выберите держателя ИП из списка", reply_markup=holders_inline_kb.holders_inline(data,'IP')      
    )"""


@router.message(Text("ПП"))
async def orders(message: Message):

    await message.answer(
        "Выберите действие с ПП: ",reply_markup=pp_inline_kb.get_pp_kb()       
    )


@router.message(Text("Снятия"))
async def orders(message: Message):

    await message.answer(
        "Выберите действие: ",reply_markup=cash_inline_kb.get_cash_kb()       
    )


@router.message(Command("get_user"))
async def get_user(msg: Message):
    user = User(*db_bank.get_user(msg.from_user.id))
    print(user.get_list())
    await msg.answer(f"Данные: {user.get_list()}")



def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
"""


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = main_kb.get_mainkb
    print(keyboard)
    await message.answer("Приветствую", reply_markup=keyboard)

@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")



@router.message(Text(text="да", ignore_case=True))
async def answer_yes(message: Message):
    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Text(text="нет", ignore_case=True))
async def answer_no(message: Message):
    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer("Это текстовое сообщение!")

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Это стикер!")

@router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer("Это GIF!")"""