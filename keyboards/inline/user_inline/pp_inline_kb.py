from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram.types import Message 
import datetime

def get_pp_kb():
    buttons = [
            [
                types.InlineKeyboardButton(text="Показать последние ПП", callback_data=f"pp_show"),
                types.InlineKeyboardButton(text="Новое ПП", callback_data=f"pp_new")
            ]            
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



def newPP_choose_date():
    builder = InlineKeyboardBuilder()
    #d = 0
    for d in range(7):
        date = datetime.date.today() - datetime.timedelta(d)
        date_string = date.strftime("%d.%m.%y")
        call = f"PP_date_{date_string}"
        
        print(call)
        builder.row(types.InlineKeyboardButton(
            text=str(date_string),
            callback_data=call,
            resize_keyboard=True)
            
        )
         
    return builder.as_markup()


def get_pp_clients(clients):
    builder = InlineKeyboardBuilder()
    for name in clients:
        call = f"PP_client_{name[1]}"
        builder.row(types.InlineKeyboardButton(
            text=f"{name[0]}",
            callback_data=f"{call}")
        )
        print(call)
    return builder.as_markup()


def get_pp_banks(banks):
    builder = InlineKeyboardBuilder()
    for name in banks:
        call = f"PP_bank_{name[1]}"
        builder.row(types.InlineKeyboardButton(
            text=f"{name[0]}",
            callback_data=f"{call}") 
        )
        print(call)
    return builder.as_markup()


def get_pp_holders(data):
    builder = InlineKeyboardBuilder()
    for nameid in data:
        
        call = f"PP_holder_{nameid[1]}"
        print(call)
        builder.row(types.InlineKeyboardButton(
            text=f"{nameid[0]}",
            callback_data=f"{call}")
            
        )
        print(call)
    return builder.as_markup()


def wallets_holder_inline(data,tp):
    builder = InlineKeyboardBuilder()
    for wallet in data:
        if tp == 'FIS':
            call = f"wallet_FIS_{wallet[0]}"
        elif tp == 'IP':
            call = f"wallet_IP_{wallet[0]}"
        
        print(call)
        builder.row(types.InlineKeyboardButton(
            text=f"{wallet[2]} / {wallet[5]} руб",
            callback_data=f"{call}",
            resize_keyboard=True)
            
        )
        print(wallet[2])
        
    return builder.as_markup()


def choose_tariff():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Изменить", callback_data=f"PP_tariff_yes"), types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"PP_tariff_no"))
    #builder.row(types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"PP_tariff_no"))
    return builder.as_markup()


def choose_add_tariff():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Изменить", callback_data=f"PP_addtariff_yes"), types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"PP_addtariff_no"))
    #builder.row(types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"PP_addtariff_no"))
    return builder.as_markup()


def choose_next_new_order():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Завершить", callback_data=f"pp_exit"), types.InlineKeyboardButton(text=f"Добавить еще ПП", callback_data=f"pp_new"))
    return builder.as_markup()


def show_pp_list(data,page):
    builder = InlineKeyboardBuilder()

    data.reverse()
    print(data)
    for order in data[page*7:(page+1)*7]:
        call = f"PP_order_{order[0]}"
        print(call)
        payed = '❌' if order[17] == 'new' else '💸' if order[17] == 'tax_payed' else '✅'
        text = f"{payed}{order[1][:-3]} {order[3]} {order[4][:-3]} {order[5]} = {order[6]}"
        builder.row(types.InlineKeyboardButton(
            text=text,
            callback_data=f"{call}")
            
        )
    if page > 0:
        builder.row(types.InlineKeyboardButton(text=f"<-",callback_data=f"PP_order_page_{page-1}"),
                    types.InlineKeyboardButton(text=f"->",callback_data=f"PP_order_page_{page+1}"))
    else:
            builder.row(types.InlineKeyboardButton(text=f"->",callback_data=f"PP_order_page_{page+1}"))

    return builder.as_markup()


def pp_actions():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Назад", callback_data=f"PP_order_page_0"), 
                types.InlineKeyboardButton(text=f"Оплата налога", callback_data=f"PP_order_tax"))
    #builder.row(types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"PP_addtariff_no"))
    return builder.as_markup()