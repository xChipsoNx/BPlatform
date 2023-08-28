from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram.types import Message 
import datetime



def get_cash_kb():
    buttons = [
            [
                types.InlineKeyboardButton(text="Показать задания", callback_data=f"cash_task"),
                types.InlineKeyboardButton(text="Показать снятия", callback_data=f"cash_show"),
                types.InlineKeyboardButton(text="Новое снятие", callback_data=f"cash_new")
            ]            
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def show_task_list(data,page):
    builder = InlineKeyboardBuilder()

    #data.reverse()
    print(data)
    for task in data[page*7:(page+1)*7]:
        call = f"cash_task_{task[0]}"
        print(call)
        status = '❌' if task[8] == 'new' else '💸' if task[8] == 'tax_payed' else '✅'
        text = f"{task[1][:-3]} {task[3]} {task[4][:-3]} = {task[5]}"
        yes = '✅'
        no = '❌'
        tomorow = '➡️'
        builder.row(types.InlineKeyboardButton(text=text,callback_data=f"{call}"),
                    types.InlineKeyboardButton(text=yes,callback_data=f"cash_task_yes"),
                    types.InlineKeyboardButton(text=no,callback_data=f"cash_task_no"),
                    types.InlineKeyboardButton(text=tomorow,callback_data=f"cash_task_tomorow")
            
        )
    if page > 0:
        builder.row(types.InlineKeyboardButton(text=f"<-",callback_data=f"cash_task_page_{page-1}"),
                    types.InlineKeyboardButton(text=f"->",callback_data=f"cash_task_page_{page+1}"))
    else:
            builder.row(types.InlineKeyboardButton(text=f"->",callback_data=f"cash_task_page_{page+1}"))

    return builder.as_markup()