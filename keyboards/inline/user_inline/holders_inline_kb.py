from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram.types import Message 
import datetime

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


def choose_lk_action(tp, id):
    if tp == 'FIS':
        buttons = [
            [
                types.InlineKeyboardButton(text="Перевод", callback_data=f"lk_FIS_transferfis_{id}"),
                types.InlineKeyboardButton(text="Вывод", callback_data=f"lk_FIS_paymentfis_{id}"),
                types.InlineKeyboardButton(text="Снятие", callback_data=f"lk_FIS_cash_{id}")
            ]            
        ]
    elif tp == 'IP':
        buttons = [
            [
                types.InlineKeyboardButton(text="Перевод себе", callback_data=f"lk_IP_transfer_{id}"),
                types.InlineKeyboardButton(text="Снятие", callback_data=f"lk_IP_cash_{id}")
            ],
            [ 
                types.InlineKeyboardButton(text="Транзит", callback_data=f"lk_IP_transit_{id}"),
                types.InlineKeyboardButton(text="Покупки", callback_data=f"lk_IP_purchases_{id}"),
                types.InlineKeyboardButton(text="Счет", callback_data=f"lk_IP_check_{id}")
            ]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def lk_confirmation_transfer():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data=f"lk_transfer_cancel"),
                (types.InlineKeyboardButton(text="Подтвердить", callback_data=f"lk_transfer_confirmation")))
    return builder.as_markup()


def back_to_wallet(data):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Нет", callback_data=f"lk_transfer_cancel"),
                (types.InlineKeyboardButton(text="Подтвердить", callback_data=data)))
    return builder.as_markup()



def cash_choose_date():
    builder = InlineKeyboardBuilder()
    #d = 0
    for d in range(7):
        date = datetime.date.today() + datetime.timedelta(d)
        date_string = date.strftime("%d.%m.%y")
        call = f"lk_cash_date_{date_string}"
        
        print(call)
        builder.row(types.InlineKeyboardButton(
            text=str(date_string),
            callback_data=call,
            resize_keyboard=True)
            
        )
         
    return builder.as_markup()

def lk_confirmation_cash():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data=f"lk_cash_cancel"),
                (types.InlineKeyboardButton(text="Подтвердить", callback_data=f"lk_cash_confirmation")))
    return builder.as_markup()


def lk_confirmation_pushcheses():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data=f"lk_pushchases_cancel"),
                (types.InlineKeyboardButton(text="Подтвердить", callback_data=f"lk_pushchases_confirmation")))
    return builder.as_markup()


def choose_transit_tariff():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Изменить", callback_data=f"lk_transit_tariff_yes"), types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"lk_transit_tariff_no"))
    #builder.row(types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"PP_tariff_no"))
    return builder.as_markup()


def choose_transit_add_tariff():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Изменить", callback_data=f"lk_transit_addtariff_yes"), types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"lk_transit_addtariff_no"))
    #builder.row(types.InlineKeyboardButton(text=f"Оставить 1%", callback_data=f"PP_addtariff_no"))
    return builder.as_markup()


def lk_transit_order_confirm():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Отмена", callback_data=f"lk_transit_confirm_exit"), types.InlineKeyboardButton(text=f"Подтвердить", callback_data=f"lk_transit_confirm_yes"))
    return builder.as_markup()


def lk_check_clients(clients):
    builder = InlineKeyboardBuilder()
    for name in clients:
        call = f"lk_check_client_{name[1]}"
        builder.row(types.InlineKeyboardButton(
            text=f"{name[0]}",
            callback_data=f"{call}")
        )
        print(call)
    return builder.as_markup()


def lk_check_confirm():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Отмена", callback_data=f"lk_check_confirm_exit"), types.InlineKeyboardButton(text=f"Подтвердить", callback_data=f"lk_check_confirm_yes"))
    return builder.as_markup()


def choose_sbp_transferfis():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Нет, внутрибанковский", callback_data=f"lk_transferfis_nosbp"), types.InlineKeyboardButton(text=f"Да, по СБП", callback_data=f"lk_transferfis_yessbp"))
    return builder.as_markup()


def choose_sbp_paymentfis():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Нет, внутрибанковский", callback_data=f"lk_paymentfis_nosbp"), types.InlineKeyboardButton(text=f"Да, по СБП", callback_data=f"lk_paymentfis_yessbp"))
    return builder.as_markup()


def get_bank_list_kb(data):

    builder = InlineKeyboardBuilder()
    for bank in data:
        call = f"lk_transferfis_bank_{bank[1]}"
        
        print(call)
        builder.row(types.InlineKeyboardButton(
            text=f"{bank[0]}",
            callback_data=f"{call}",
            resize_keyboard=True)
            
        )
        
    return builder.as_markup()


def lk_transferfis_confirm():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Отмена", callback_data=f"lk_transferfis_confirm_exit"), types.InlineKeyboardButton(text=f"Подтвердить", callback_data=f"lk_transferfis_confirm_yes"))
    return builder.as_markup()


"""def get_wallets_from_bank(data):
    builder = InlineKeyboardBuilder()
    for wallet in data:
        call = f"wallet_FIS_{wallet[0]}"
        print(call)
        builder.row(types.InlineKeyboardButton(
            text=f"{wallet[2]} / {wallet[5]} руб",
            callback_data=f"{call}",
            resize_keyboard=True)
            
        )
        print(wallet[2])
        
    return builder.as_markup()"""


def wallets_holder_for_transferfis(data, err):
    builder = InlineKeyboardBuilder()
    for wallet in data:
        if str(wallet[0]) != err:
            call = f"twallet_FIS_{wallet[0]}"
            print(call, err)
            builder.row(types.InlineKeyboardButton(
                text=f"{wallet[2]} {wallet[3]} == {wallet[5]} руб",
                callback_data=f"{call}",
                resize_keyboard=True)
                
            )
            print(wallet[2])
        
    return builder.as_markup()


def lk_payments_client(data):
    builder = InlineKeyboardBuilder()
    for client in data:
        print(client)
        call = f"pclient_{client[1]}_{client[0]}"
        builder.row(types.InlineKeyboardButton(
            text=f"{client[0]}",
            callback_data=f"{call}",
            resize_keyboard=True)
            
        )
        print(client[1])
        
    return builder.as_markup()