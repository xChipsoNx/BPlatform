from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram.types import Message 


def holders_inline(data, tp):
    builder = InlineKeyboardBuilder()
    for nameid in data:
        if tp == 'FIS':
            call = f"holder_FIS_{nameid[1]}"
        elif tp == 'IP':
            call = f"holder_IP_{nameid[1]}"
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


def choose_lk_action(tp):
    if tp == 'FIS':
        buttons = [
            [
                types.InlineKeyboardButton(text="Перевод", callback_data=f"lk_FIS_remittance"),
                types.InlineKeyboardButton(text="Снятие", callback_data=f"lk_FIS_cash")
            ]            
        ]
    elif tp == 'IP':
        buttons = [
            [
                types.InlineKeyboardButton(text="Перевод", callback_data=f"lk_IP_remittance"),
                types.InlineKeyboardButton(text="Снятие", callback_data=f"lk_IP_cash")
            ],
            [ 
                types.InlineKeyboardButton(text="Счёт", callback_data=f"lk_IP_check"),
                types.InlineKeyboardButton(text="Покупки", callback_data=f"lk_IP_purchases")
            ]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


