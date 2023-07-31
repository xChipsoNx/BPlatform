from aiogram import F, Router, types
from aiogram.types import Message 
from aiogram.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router
#from keyboards.default import main_kb as mm
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from loader import db_bank
from utils.user_cls import User
from keyboards.inline.user_inline import holders_inline


router = Router()  # [1]

@router.message(Command("start"))
async def start_handler(msg: Message):
    kb = [
        [
            types.KeyboardButton(text="ФИЗ"),
            types.KeyboardButton(text="ИП")
        ],
        [
            types.KeyboardButton(text="ПП")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню"
    )
    db_bank.new_user(msg.from_user.id)
    
    await msg.answer("Привет! Я банк платформа",reply_markup=keyboard)


@router.message(Text("ФИЗ"))
async def fis_holders(message: Message):
    data = db_bank.get_name_holders("'ФИЗ'")
    await message.answer(
        "Выберите держателя физ из списка:", reply_markup=holders_inline.holders_fis_inline(data)       
    )


@router.message(Text("ИП"))
async def ip_holders(message: Message):
    await message.answer(
        "Выберите держателя из списка"       
    )

@router.message(Text("ПП"))
async def orders(message: Message):
    await message.answer(
        "Выберите держателя из списка"       
    )

@router.message(Command("get_user"))
async def get_user(msg: Message):
    user = User(*db_bank.get_user(2084313004))
    print(user.get_list())
    await msg.answer(f"Данные: {user.get_list()}")

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