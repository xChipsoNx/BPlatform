from aiogram import F, Router, types
from aiogram.types import Message 
from aiogram.filters import Command, Text
from aiogram import Router
from loader import db_bank
from utils.user_cls import User, Wallet
from keyboards.inline.user_inline import holders_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()  



@router.callback_query(Text(startswith="holder_"))
async def get_wallets(callback: types.CallbackQuery):
    action = callback.data.split("_")
    hold_id = action[2]

    if action[1] == 'FIS':
        wal = db_bank.get_walets(hold_id, "'ФИЗ'")
        kb = holders_inline_kb.wallets_holder_inline(wal,'FIS')
    elif action[1] == 'IP':
        wal = db_bank.get_walets(hold_id, "'ИП'")
        kb = holders_inline_kb.wallets_holder_inline(wal,'IP')
    name = wal[0][3]
    await callback.message.answer(
        f"{name} Выберите кошелек держателя физ из списка:", reply_markup=kb  
    )


@router.callback_query(Text(startswith="wallet_"))
async def look_wallet(callback: types.CallbackQuery):
    action = callback.data.split("_")
    wal_id = action[2]
    print(action)
    if action[1] == 'FIS':
        kb = holders_inline_kb.choose_lk_action('FIS')
    elif action[1] == 'IP':
        kb = holders_inline_kb.choose_lk_action('IP')

    lk = Wallet(*db_bank.get_lk_wallet(wal_id))    
    await callback.message.answer(
        f"{lk.type} {lk.holder_name} {lk.bank}\nБалланс: {lk.balance}\nВыберите действие с кошелеком держателя физ из списка:", reply_markup=kb     
    )


@router.callback_query(Text(startswith="lk_"))
async def look_wallet(callback: types.CallbackQuery):
    action = callback.data.split("_")
    print(action)
    if action[1] == 'FIS':
        if action[2] == "remittance":
            print('pjkupka')
        elif action[2] == "cash":
            pass
        
    if action[1] == 'IP':
        if action[2] == "remittance":
            print('pjkupka2')
            pass
        elif action[2] == "cash":
            pass
        elif action[2] == "check":
            pass
        elif action[2] == "purchases":
            pass


