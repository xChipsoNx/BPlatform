from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram import F, types, Router

#router = Router()

#markup_main = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(' Wallets '))


def get_mainkb():
    kb = [
        [
            types.KeyboardButton(text="Держатели"),
            types.KeyboardButton(text="ПП")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        #input_field_placeholder="Добро пожаловать в банковскую систему"
    )
    print(keyboard)
    return keyboard

"""

def get_mainkb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Держатели")
    kb.button(text="ПП")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)

def get_mainkb():
    kb = [
        [
            types.KeyboardButton(text="Держатели"),
            types.KeyboardButton(text="ПП")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        #input_field_placeholder="Добро пожаловать в банковскую систему"
    )
    print(keyboard)
    return keyboard

@router.message(Command("reply_builder"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
"""


"""@router.message(Command("inline_url"))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Оф. канал Telegram",
        url="tg://resolve?domain=telegram")
    )

    # Чтобы иметь возможность показать ID-кнопку,
    # У юзера должен быть False флаг has_private_forwards
    user_id = 1234567890
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Какой-то пользователь",
            url=f"tg://user?id={user_id}")
        )

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )

@router.callback_query(Text("random_value"))
async def send_random_value(callback: types.CallbackQuery): 
    await callback.message.answer(str(randint(1, 10)))


builder = InlineKeyboardBuilder()
for i in range(15):

    builder.button(text=f"Кнопка {i}”, callback_data=f”button_{i}")

builder.adjust(2)
await msg.answer("Текст сообщения", reply_markup=builder.as_markup())"""