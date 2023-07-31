from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram.types import Message 


def holders_fis_inline(data):
    builder = InlineKeyboardBuilder()
    for nameid in data:
        call = f"holder_{nameid[1]}"
        print(call)
        builder.row(types.InlineKeyboardButton(
            text=f"{nameid[0]}",
            callback_data=f"{call}")
        )
        print(nameid)
    return builder.as_markup()