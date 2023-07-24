from aiogram import F, Router, types
from aiogram.types import Message 
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from keyboards.default import main_kb




router = Router()  # [1]

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = main_kb.get_mainkb
    print(keyboard)
    await message.answer("Приветствую", reply_markup=keyboard)

"""
@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")



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