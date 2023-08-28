from aiogram import F, Router, types
from aiogram.types import Message 
from aiogram.filters import Command, Text
from aiogram import Router
from loader import db_bank
from utils.user_cls import User, Wallet, PP
from keyboards.inline.user_inline import holders_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import datetime, math

router = Router()  

class LKstates(StatesGroup):
    lk_remitance = State()
    lk_remitance_sum = State()
    lk_confirmation_remitance = State()

    lk_cash = State()
    lk_cash_sum = State()
    lk_confirmation_cash = State()

    lk_check = State()
    lk_check_sum = State()
    lk_check_confirm = State()

    lk_pushchases = State()
    lk_pushchases_sum = State()
    lk_confirmation_pushchases = State()

    lk_actions = State()
    lk_choose_holder = State()
    lk_choose_wallet = State()

    lk_transit = State()
    lk_transit_choose_wallet = State()
    lk_transit_sum = State()
    lk_transit_tariff = State()
    lk_transit_add_tariff = State()
    lk_transit_result = State()
    lk_transit_confirm = State()

    lk_transferfis_sbp = State()
    lk_transferfis_holder = State()
    lk_transferfis_bank = State()
    lk_transferfis_sum = State()
    lk_transferfis_confirm = State()

    lk_paymentfis_sbp = State()
    lk_paymentfis_client = State()
    lk_paymentfis_sum = State()
    lk_paymentfis_confirm = State()

     
    

async def look_wallet(callback, state, data):
    action = data.split("_")
    wal_id = action[2]
    await state.update_data(lk_wal_id=wal_id)
    print(action)

    if action[1] == 'FIS':
        kb = holders_inline_kb.choose_lk_action('FIS', wal_id)
    elif action[1] == 'IP':
        kb = holders_inline_kb.choose_lk_action('IP',wal_id)
    
    lk = Wallet(*db_bank.get_lk_wallet(wal_id)) 
    
    await state.update_data(lk_wal_bank=lk.bank,lk_wal_bank_id = lk.bank_id)

    await callback.message.answer(
        f"{lk.holder_name} {lk.bank}\nБалланс: {lk.balance}\nВыберите действие с кошелеком держателя из списка:", reply_markup=kb     
    )

    await state.set_state(LKstates.lk_actions)


@router.callback_query(LKstates.lk_choose_wallet, Text(startswith="wallet_"))
async def lk_menu(callback: types.CallbackQuery,  state: FSMContext):
    await look_wallet(callback, state, callback.data)



@router.callback_query(LKstates.lk_actions, Text(startswith="lk_"))
async def lk_actions(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")
    
    tx = await state.get_data()

    if action[1] == 'FIS':
        await state.update_data(lk_type=action[1])
        if action[2] == "transferfis":
            await callback.message.answer(
                f"Перевод по СБП?",
                reply_markup=holders_inline_kb.choose_sbp_transferfis()
            )
            await state.set_state(LKstates.lk_transferfis_sbp)
        elif action[2] == "paymentfis":
            await callback.message.answer(
                f"Выплата по СБП?",
                reply_markup=holders_inline_kb.choose_sbp_paymentfis()
            )
            await state.set_state(LKstates.lk_paymentfis_sbp)
        elif action[2] == "cash":
            await callback.message.answer(
                f"Выберите дату снятия:",
                reply_markup=holders_inline_kb.cash_choose_date()
            )
            print(tx)
            await state.set_state(LKstates.lk_cash)

        
    if action[1] == 'IP':
        await state.update_data(lk_type=action[1])
        if action[2] == "transfer":
            wal = db_bank.get_walets(tx['lk_holder_id'], "'FIS'")
            await callback.message.answer(
                f"Выберите банк физ держателя {tx['lk_from_holder_name'][2:]} для перевода из списка:",
                reply_markup = holders_inline_kb.wallets_holder_inline(wal,'FIS')
            )
            print(tx)
            await state.set_state(LKstates.lk_remitance)
            
        elif action[2] == "cash":
            await callback.message.answer(
                f"Выберите дату снятия:",
                reply_markup=holders_inline_kb.cash_choose_date()
            )
            print(tx)
            await state.set_state(LKstates.lk_cash)

        elif action[2] == "check":
            await callback.message.answer(
                f"Выберите клиента для оплаты счёта:",
                reply_markup=holders_inline_kb.lk_check_clients(db_bank.get_clients_list())                
            )
            print(tx)
            await state.set_state(LKstates.lk_check)

        elif action[2] == "purchases":
            await callback.message.answer(
                f"Введите сумму покупки:"                
            )
            print(tx)
            await state.set_state(LKstates.lk_pushchases_sum)

        elif action[2] == "transit":
            data = db_bank.get_name_holders("'IP'")
            await callback.message.answer(
                "Выберите держателя ИП из списка для транзита:", reply_markup=holders_inline_kb.holders_inline(data,'IP')      
            )
            await state.set_state(LKstates.lk_transit)


@router.callback_query(LKstates.lk_transferfis_sbp, Text(startswith="lk_transferfis_"))
async def lk_transferfis_sbp(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split("_")[2])
    tx = await state.get_data()
    print(tx)
    if callback.data.split("_")[2] == "nosbp":
        await state.update_data(lk_transferfis_sbp='nosbp')
        data = db_bank.get_wallets_from_bank(tx['lk_wal_bank_id'])
        print(data)
        await callback.message.answer(
            text="Выбран внутрибанковский перевод. Выберите держателя:",
            reply_markup=holders_inline_kb.wallets_holder_for_transferfis(data,tx['lk_wal_id'])
        )

        await state.set_state(LKstates.lk_transferfis_holder)
    
    elif callback.data.split("_")[2] == "yessbp":
        await state.update_data(lk_transferfis_sbp='sbp')
        data = db_bank.get_banks_list("'FIS'")
        await callback.message.answer(
            text="Выбран перевод по СБП. Выберите банк:",
            reply_markup=holders_inline_kb.get_bank_list_kb(data)
        )
        await state.set_state(LKstates.lk_transferfis_bank)


@router.callback_query(LKstates.lk_transferfis_bank, Text(startswith="lk_transferfis_bank_"))
async def lk_transferfis_bank(callback: types.CallbackQuery, state: FSMContext):
    bank_id = callback.data.split("_")[3]
    #await state.update_data(lk_transferfis_bank_id=callback.data.split("_")[3])
    data = db_bank.get_wallets_from_bank(bank_id)
    await callback.message.answer(
        text="Выбран банк для перевода по СБП. Выберите держателя:",
        reply_markup=holders_inline_kb.wallets_holder_for_transferfis(data,bank_id)
    )
    await state.set_state(LKstates.lk_transferfis_holder)


@router.callback_query(LKstates.lk_transferfis_holder, Text(startswith="twallet_FIS_"))
async def lk_tranferfis_holder(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split("_")[2])
    await state.update_data(lk_transferfis_wal_id=callback.data.split("_")[2])
    await callback.message.answer(
        text="Выбран держатель для перевода по СБП. Введите сумму:"
    )
    await state.set_state(LKstates.lk_transferfis_sum)


@router.message(LKstates.lk_transferfis_sum)
async def lk_transferfis_sum(message: Message, state: FSMContext):
    await state.update_data(lk_transferfis_sum=message.text.lower())
    print(message.text.format())
    tx = await state.get_data()
    lk = Wallet(*db_bank.get_lk_wallet(tx['lk_wal_id'])) 
    transfer_lk = Wallet(*db_bank.get_lk_wallet(tx['lk_transferfis_wal_id']) )

    print(tx)
    if tx['lk_transferfis_sbp'] == 'nosbp':
        #await state.update_data(lk_transferfis_bank_id=lk.bank_id)
        await message.answer(
            f"{tx['lk_from_holder_name']}\nВнутренний перевод {lk.bank} держателю {transfer_lk.holder_name} на сумму: {tx['lk_transferfis_sum']}.\nВы подтверждаете перевод?",
            reply_markup=holders_inline_kb.lk_transferfis_confirm()
        )
    elif tx['lk_transferfis_sbp'] == 'sbp':
        await message.answer(
            f"{tx['lk_from_holder_name']}\nПеревод по СБП в {transfer_lk.bank} держателю {transfer_lk.holder_name} на сумму: {tx['lk_transferfis_sum']}.\nВы подтверждаете перевод?",
            reply_markup=holders_inline_kb.lk_transferfis_confirm()
        )
    await state.update_data(lk_transferfis_wal_id=transfer_lk.id)
    await state.set_state(LKstates.lk_transferfis_confirm)


@router.callback_query(LKstates.lk_transferfis_confirm, Text(startswith="lk_transferfis_confirm_"))
async def lk_transferfis_result(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    acc = action[3]
    tx = await state.get_data()
    holder = tx['lk_holder_id']
    name = tx['lk_from_holder_name']

    if acc == "yes":
        tranfer_type = f"transfer_{tx['lk_transferfis_sbp']}"
        db_bank.add_new_transfer(tx['lk_wal_id'], tx['lk_transferfis_wal_id'], tx['lk_transferfis_sum'], tranfer_type)
        await callback.message.answer(
            f"Перевод исполнен успешно! Возврат в кошелек."
        )  
    elif acc == "exit":
        await callback.message.answer(
            f"Перевод отменен! Возврат в кошелек."
        )
    await state.clear()
    await state.set_state(LKstates.lk_choose_wallet)
    await state.update_data(lk_holder_id=holder)
    await state.update_data(lk_from_holder_name=name)
    await look_wallet(callback, state, f"wallet_FIS_{tx['lk_wal_id']}")


@router.callback_query(LKstates.lk_paymentfis_sbp, Text(startswith="lk_paymentfis_"))
async def lk_paymentfis_sbp(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split("_")[2])
    data = db_bank.get_clients_list()
    if callback.data.split("_")[2] == "yessbp":
        await state.update_data(lk_sbp='sbp')
        await callback.message.answer(
            text="Выбран перевод по СБП. Выберите клиента:",
            reply_markup=holders_inline_kb.lk_payments_client(data)
        )
    elif callback.data.split("_")[2] == "nosbp":
        await state.update_data(lk_sbp='nosbp')
        await callback.message.answer(
            text="Выбран внутрибанковский перевод. Выберите клиента:",
            reply_markup=holders_inline_kb.lk_payments_client(data)
        )

    await state.set_state(LKstates.lk_paymentfis_client)


@router.callback_query(LKstates.lk_paymentfis_client, Text(startswith="pclient_"))
async def lk_payment_client(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    await state.update_data(lk_client_id=action[1], lk_client_name = action[2])

    await callback.message.answer(
        f"Введите сумму выплаты клиенту:"    
    )

    await state.set_state(LKstates.lk_paymentfis_sum)


@router.message(LKstates.lk_paymentfis_sum)
async def lk_paymentfis_sum(message: Message, state: FSMContext):
    await state.update_data(lk_paymentfis_sum=message.text.lower())
    print(message.text.format())
    tx = await state.get_data()
    lk = Wallet(*db_bank.get_lk_wallet(tx['lk_wal_id'])) 
    
    if tx['lk_sbp'] == 'nosbp':
        #await state.update_data(lk_transferfis_bank_id=lk.bank_id)
        await message.answer(
            f"{tx['lk_from_holder_name']}\nВнутренний перевод клиенту на сумму: {tx['lk_paymentfis_sum']}.\nВы подтверждаете перевод?",
            reply_markup=holders_inline_kb.lk_transferfis_confirm()
        )
    elif tx['lk_sbp'] == 'sbp':
        await message.answer(
            f"{tx['lk_from_holder_name']}\nПеревод по СБП клиенту на сумму: {tx['lk_paymentfis_sum']}.\nВы подтверждаете перевод?",
            reply_markup=holders_inline_kb.lk_transferfis_confirm()
        )
    await state.set_state(LKstates.lk_paymentfis_confirm)

########
@router.callback_query(LKstates.lk_paymentfis_confirm, Text(startswith="lk_transferfis_confirm_"))
async def lk_paymentfis_result(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    acc = action[3]
    tx = await state.get_data()
    holder = tx['lk_holder_id']
    name = tx['lk_from_holder_name']

    if acc == "yes":
        tranfer_type = f"payment_{tx['lk_sbp']}"
        print(tx['lk_client_name'], tx['lk_from_holder_name'], tx['lk_wal_bank'], tx['lk_paymentfis_sum'], tx['lk_client_id'], tx['lk_wal_id'],  tranfer_type)
        db_bank.add_new_payment(tx['lk_client_name'], tx['lk_from_holder_name'], tx['lk_wal_bank'], tx['lk_paymentfis_sum'], tx['lk_client_id'], tx['lk_wal_id'],  tranfer_type)
        await callback.message.answer(
            f"Перевод исполнен успешно! Возврат в кошелек."
        )  
    elif acc == "exit":
        await callback.message.answer(
            f"Перевод отменен! Возврат в кошелек."
        )
    await state.clear()
    await state.set_state(LKstates.lk_choose_wallet)
    await state.update_data(lk_holder_id=holder)
    await state.update_data(lk_from_holder_name=name)
    await look_wallet(callback, state, f"wallet_FIS_{tx['lk_wal_id']}")


@router.callback_query(LKstates.lk_remitance, Text(startswith="wallet_FIS_"))
async def lk_transfer_fis_wallet(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    wal_id = action[2]
    lk = Wallet(*db_bank.get_lk_wallet(wal_id)) 
    await state.update_data(lk_fis_id=wal_id)
    await state.update_data(lk_fis_bank_name=lk.bank)
    print(action)

    await callback.message.answer(
        f"Введите сумму перевода себе на физ счет {lk.bank}:"    
    )

    await state.set_state(LKstates.lk_remitance_sum)

###
@router.message(LKstates.lk_remitance_sum)
async def lk_confirmation_remitance(message: Message, state: FSMContext):
    await state.update_data(lk_transfer_sum=message.text.lower())
    print(message.text.format())
    tx = await state.get_data()
    
    print(tx)
    await message.answer(
        f"{tx['lk_from_holder_name']}\nПеревод с {tx['lk_wal_bank']} на {tx['lk_fis_bank_name']} на сумму: {tx['lk_transfer_sum']}.\nВы подтверждаете перевод?",
        reply_markup=holders_inline_kb.lk_confirmation_transfer()
    )
    await state.set_state(LKstates.lk_confirmation_remitance)


@router.callback_query(LKstates.lk_confirmation_remitance, Text(startswith="lk_transfer_"))
async def lk_transfer_result(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    acc = action[2]
    tx = await state.get_data()
    holder = tx['lk_holder_id']
    name = tx['lk_from_holder_name']

    if acc == "confirmation":
        db_bank.add_new_transfer(tx['lk_wal_id'], tx['lk_fis_id'], tx['lk_transfer_sum'], 'transfer')
        await callback.message.answer(
            f"Перевод исполнен успешно! Возврат в кошелек."
        )  
    elif acc == "cancel":
        await callback.message.answer(
            f"Перевод отменен! Возврат в кошелек."
        )
    await state.clear()
    await state.set_state(LKstates.lk_choose_wallet)
    await state.update_data(lk_holder_id=holder)
    await state.update_data(lk_from_holder_name=name)
    await look_wallet(callback, state, f"wallet_IP_{tx['lk_wal_id']}")
    



@router.callback_query(LKstates.lk_cash, Text(startswith="lk_cash_date_"))
async def lk_cash_choose_date(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    date = action[3]
    print(date)
    await state.update_data(lk_cash_date=date)
    print(action)

    await callback.message.answer(
        f"Введите сумму снятия:"    
    )
    await state.set_state(LKstates.lk_cash_sum)


@router.message(LKstates.lk_cash_sum)
async def lk_cash_sum(message: Message, state: FSMContext):
    await state.update_data(lk_cash_sum=message.text.lower())
    print(message.text.format())
    tx = await state.get_data()
    lk = Wallet(*db_bank.get_lk_wallet(tx['lk_wal_id'])) 
    print(tx)
    await message.answer(
        f"{tx['lk_from_holder_name']}\nСнятие с {lk.bank} на сумму: {tx['lk_cash_sum']}.\nВы подтверждаете снятие?",
        reply_markup=holders_inline_kb.lk_confirmation_cash()
    )
    await state.set_state(LKstates.lk_confirmation_cash)


@router.callback_query(LKstates.lk_confirmation_cash, Text(startswith="lk_cash_"))
async def lk_cash_result(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    acc = action[2]
    tx = await state.get_data()
    lk = Wallet(*db_bank.get_lk_wallet(tx['lk_wal_id'])) 
    hold_id = tx['lk_holder_id']
    #name = tx['lk_from_holder_name']

    if acc == "confirmation":
        db_bank.add_new_cash_task(tx['lk_cash_date'], lk.type, lk.holder_name, lk.bank, tx['lk_cash_sum'], tx['lk_wal_id'], lk.bank_id )
        await callback.message.answer(
            f"Задание на снятие добавлено успешно! Возврат в кошелек."
        )  
    elif acc == "cancel":
        await callback.message.answer(
            f"Задание на снятие отменен! Возврат в кошелек."
        )
    await state.clear()
    await state.set_state(LKstates.lk_choose_wallet)
    await state.update_data(lk_holder_id=hold_id)
    await state.update_data(lk_wal_id=lk.id)
    await state.update_data(lk_from_holder_name=lk.holder_name)
    await look_wallet(callback, state, f"wallet_{tx['lk_type']}_{tx['lk_wal_id']}")


@router.message(LKstates.lk_pushchases_sum)
async def lk_pushchases_sum(message: Message, state: FSMContext):
    await state.update_data(lk_pushchases_sum=message.text.lower())
    print(message.text.format())
    tx = await state.get_data()
    lk = Wallet(*db_bank.get_lk_wallet(tx['lk_wal_id'])) 
    print(tx)
    await message.answer(
        f"{tx['lk_from_holder_name']}\nПокупка с {lk.bank} на сумму: {tx['lk_pushchases_sum']}.\nВы подтверждаете покупку?",
        reply_markup=holders_inline_kb.lk_confirmation_pushcheses()
    )
    await state.set_state(LKstates.lk_confirmation_pushchases)


@router.callback_query(LKstates.lk_confirmation_pushchases, Text(startswith="lk_pushchases_"))
async def lk_cash_result(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    acc = action[2]
    tx = await state.get_data()
    
    holder = tx['lk_wal_id']
    name = tx['lk_from_holder_name']
    hold_id = tx['lk_holder_id']
    if acc == "confirmation":
        db_bank.add_new_pushchases(tx['lk_pushchases_sum'], tx['lk_wal_id'])
        await callback.message.answer(
            f"Покупка добавлена успешно! Возврат в кошелек."
        )  
    elif acc == "cancel":
        await callback.message.answer(
            f"Покупка отменена! Возврат в кошелек."
        )
    await state.clear()
    await state.set_state(LKstates.lk_choose_wallet)
    await state.update_data(lk_wal_id=holder)
    await state.update_data(lk_from_holder_name=name)
    await state.update_data(lk_holder_id=hold_id)
    await look_wallet(callback, state, f"wallet_{tx['lk_type']}_{tx['lk_wal_id']}")


@router.callback_query(LKstates.lk_transit,Text(startswith="holder_IP_"))
async def get_transit_holders(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")
    hold_id = action[2]
    await state.update_data(lk_transit_holder_id=hold_id)

    wal = db_bank.get_walets(hold_id, "'IP'")
    kb = holders_inline_kb.wallets_holder_inline(wal,'IP')

    name = wal[0][3]
    await state.update_data(lk_transit_to_holder_name=name)

    await callback.message.answer(
        f"{name} Выберите кошелек держателя для транзита из списка:", reply_markup=kb  
    )
    await state.set_state(LKstates.lk_transit_choose_wallet)


@router.callback_query(LKstates.lk_transit_choose_wallet, Text(startswith="wallet_IP_"))
async def lk_transit_ip_wallet(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    wal_id = action[2]
    lk = Wallet(*db_bank.get_lk_wallet(wal_id)) 
    await state.update_data(lk_transit_id=wal_id)
    await state.update_data(lk_transit_bank_name=lk.bank, lk_transit_bank_id = lk.bank_id)
    print(action)

    await callback.message.answer(
        f"Введите сумму перевода себе на физ счет {lk.bank}:"    
    )

    await state.set_state(LKstates.lk_transit_sum)


@router.message(LKstates.lk_transit_sum)
async def lk_transit_new_enter_sum(message: Message, state: FSMContext):
    await state.update_data(lk_transit_sum=message.text.lower())
    print(message.text.format())
    
    await message.answer(
        f"По умолчанию, процент банка устанволен 1%. Хотите изменить?:", reply_markup=holders_inline_kb.choose_transit_tariff()
    )
    await state.set_state(LKstates.lk_transit_tariff)


@router.callback_query(LKstates.lk_transit_tariff, Text(startswith="lk_transit_tariff_"))
async def lk_transit_new_choose_tariff(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split("_")[2])

    if callback.data.split("_")[3] == "no":
        await state.update_data(lk_transit_tariff=0.01)
        await callback.message.answer(
        f"Процент банка устанволен 1% ! \nДополнительный процент, по умолчанию установлен 1%. \nХотите изменить?:",
        reply_markup=holders_inline_kb.choose_transit_add_tariff()
    )
        await state.set_state(LKstates.lk_transit_add_tariff)
    elif callback.data.split("_")[3] == "yes":
         await callback.message.answer(text="Теперь, пожалуйста, введите процент банка, в формате 1 = 1% :"
    )

@router.message(LKstates.lk_transit_tariff)
async def lk_transit_new_enter_tariff(message: Message, state: FSMContext):
    await state.update_data(lk_transit_tariff=float(message.text.lower())/100)
    print(message.text.format())
    tx = await state.get_data()
    print(tx)
    await message.answer(
        text=f"Банковский процент ={tx['lk_transit_tariff']} \nДополнительный процент, по умолчанию установлен 1%. \nХотите изменить?:", 
        reply_markup=holders_inline_kb.choose_transit_add_tariff()
    )
    await state.set_state(LKstates.lk_transit_add_tariff)


@router.callback_query(LKstates.lk_transit_add_tariff, Text(startswith="lk_transit_addtariff_"))
async def lk_transit_new_choose_add_tariff(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split("_")[3])

    if callback.data.split("_")[3] == "no":
        await state.update_data(lk_transit_add_tariff=0.01)
        await callback.message.answer(
        f"Дополнительный процент банка устанволен 1%!"
        )

        await callback.message.answer(
            text="Если все верно, подтвердите запись:",
            reply_markup=holders_inline_kb.lk_transit_order_confirm()
        )
        await state.set_state(LKstates.lk_transit_confirm)
    elif callback.data.split("_")[3] == "yes":
        await callback.message.answer(text="Теперь, пожалуйста, введите дополнительный процент, в формате 1 = 1% :"
        )


@router.message(LKstates.lk_transit_add_tariff)
async def lk_transit_new_enter_add_tariff(message: Message, state: FSMContext):
    await state.update_data(lk_transit_add_tariff=float(message.text.lower())/100)
    await message.answer(
        text=f"Дополнительный процент установлен {float(message.text.lower())/100}%!"
    )
    await message.answer(
            text="Если все верно, подтвердите запись:",
            reply_markup=holders_inline_kb.lk_transit_order_confirm()
    )
    await state.set_state(LKstates.lk_transit_confirm)
    


@router.callback_query(LKstates.lk_transit_confirm, Text(startswith="lk_transit_confirm_"))
async def lk_transit_write_new_order(callback: types.CallbackQuery, state: FSMContext):
    
    if callback.data.split("_")[3] == "yes":
        tx = await state.get_data()

        sum = float(tx['lk_transit_sum'])
        tariff = float(tx['lk_transit_tariff'])
        add_tariff = float(tx['lk_transit_add_tariff'])
        tax =  math.ceil(sum /100)
        total = sum-(sum*tariff)-(sum*add_tariff)-tax
        date = datetime.date.today()
        date_string = date.strftime("%d.%m.%y")
        name = tx['lk_from_holder_name']
        hold_id=tx['lk_holder_id']
        wal_id = tx['lk_wal_id']

        client_sum = sum
        holder_sum = total 
        
        order = PP(None,date_string, 0, tx['lk_from_holder_name'],tx['lk_transit_to_holder_name'],tx['lk_transit_bank_name'], sum, tariff, add_tariff, tax, total, 0, date_string, tx['lk_wal_id'],tx['lk_transit_holder_id'],tx['lk_transit_bank_id'], tx['lk_transit_id'])
        print(order.get_list())
        ans = db_bank.add_new_order(order.get_list(), client_sum,holder_sum,"transit")
        print(ans)
        await callback.message.answer(
            f"Запись пп транзита прошла успешно! Возврат в кошелек."
        )
    elif callback.data.split("_")[3] == "exit":
        await callback.message.answer(
            f"Запись пп транзита отменена! Возврат в кошелек."
        )
    await state.clear()
    await state.set_state(LKstates.lk_choose_wallet)
    await state.update_data(lk_wal_id=wal_id)
    await state.update_data(lk_from_holder_name=name)
    await state.update_data(lk_holder_id=hold_id)
    await look_wallet(callback, state, f"wallet_{tx['lk_type']}_{tx['lk_wal_id']}")
    #ans = db_bank.add_new_order(order.get_list(), client_sum,holder_sum)
    

@router.callback_query(LKstates.lk_check, Text(startswith="lk_check_client_"))
async def lk_check_choose_client(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    client_id = action[3]
    await state.update_data(lk_check_client=client_id)
    await callback.message.answer(
        f"Введите сумму счёта:"    
    )

    await state.set_state(LKstates.lk_check_sum)


@router.message(LKstates.lk_check_sum)
async def lk_check_enter_sum(message: Message, state: FSMContext):
    await state.update_data(lk_check_sum=message.text.lower())
    print(message.text.format())
    tx = await state.get_data()
    client = db_bank.get_client_info(tx['lk_check_client'])
    print(client[0][1])
    wal = Wallet(*db_bank.get_lk_wallet(tx["lk_wal_id"]))
    
    await message.answer(
        f"Вы оплачиваете c {wal.holder_name} {wal.bank} счет на сумму: {tx['lk_check_sum']} \nв пользу клиента {client[0][1]}.\nВсе верно?", reply_markup=holders_inline_kb.lk_check_confirm()
    )
    await state.update_data(lk_check_client_name=client[0][1])
    await state.set_state(LKstates.lk_check_confirm)


@router.callback_query(LKstates.lk_check_confirm, Text(startswith="lk_check_confirm"))
async def lk_check_result(callback: types.CallbackQuery,  state: FSMContext):
    action = callback.data.split("_")
    acc = action[3]
    tx = await state.get_data()
    lk = Wallet(*db_bank.get_lk_wallet(tx['lk_wal_id'])) 
    hold_id = tx['lk_holder_id']
    #name = tx['lk_from_holder_name']

    if acc == "yes":
        db_bank.add_new_payment(tx['lk_check_client_name'], lk.holder_name, lk.bank, tx['lk_check_sum'], tx['lk_check_client'], lk.id, "check" )
        await callback.message.answer(
            f"Оплата счета добавлена успешно! Возврат в кошелек."
        )  
    elif acc == "exit":
        await callback.message.answer(
            f"Оплата счета отменена! Возврат в кошелек."
        )
    await state.clear()
    await state.set_state(LKstates.lk_choose_wallet)
    await state.update_data(lk_holder_id=hold_id)
    await state.update_data(lk_wal_id=lk.id)
    await state.update_data(lk_from_holder_name=lk.holder_name)
    await look_wallet(callback, state, f"wallet_{tx['lk_type']}_{tx['lk_wal_id']}")




@router.callback_query(Text(startswith="holder_"))
async def get_wallets(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LKstates.lk_choose_holder)
    action = callback.data.split("_")
    hold_id = action[2]
    await state.update_data(lk_holder_id=hold_id)

    if action[1] == 'FIS':
        wal = db_bank.get_walets(hold_id, "'FIS'")
        kb = holders_inline_kb.wallets_holder_inline(wal,'FIS')
    elif action[1] == 'IP':
        wal = db_bank.get_walets(hold_id, "'IP'")
        kb = holders_inline_kb.wallets_holder_inline(wal,'IP')

    name = wal[0][3]
    await state.update_data(lk_from_holder_name=name)

    await callback.message.answer(
        f"{name} Выберите кошелек держателя из списка:", reply_markup=kb  
    )
    await state.set_state(LKstates.lk_choose_wallet)