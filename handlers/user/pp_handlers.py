from aiogram import F, Router, types
from aiogram.types import Message 
from aiogram.filters import Command, Text
from aiogram import Router
from loader import db_bank
from utils.user_cls import User, Wallet, PP
from keyboards.inline.user_inline import holders_inline_kb, pp_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import math, datetime

router = Router()


class PPWork(StatesGroup):
    choosing_pp = State()
    new_pp_date = State()
    new_pp_number = State()
    choose_client = State()
    choose_bank = State()
    choose_holder = State()
    new_pp_sum = State()
    new_pp_tariff = State()
    new_pp_add_tariff = State()
    show_new_pp = State()
    

def write_new_order(pp):
    
    print(pp)
    client, wallet = db_bank.get_full_pp_info(pp['pp_client'], pp['pp_bank'], pp['pp_holder'])
    sum = float(pp['pp_sum'])
    tariff = float(pp['pp_tariff'])
    add_tariff = float(pp['pp_add_tariff'])
    tax =  math.ceil(sum /100)
    total = sum-(sum*tariff)-(sum*add_tariff)-tax
    
    date = datetime.datetime.strptime(pp['pp_date'], '%d.%m.%y')
    c_date = date + datetime.timedelta(client[3])
    close_date = c_date.strftime('%d.%m.%y')
    
    client_sum = sum - sum*float(client[2])
    holder_sum = total 
    
    order = PP(None,pp['pp_date'], pp['pp_number'], client[1],wallet[1],wallet[0], sum, tariff, add_tariff, tax, total, 0, close_date, client[0],pp['pp_holder'],pp['pp_bank'], wallet[2])
    
    ans = db_bank.add_new_order(order.get_list(), client_sum,holder_sum,"order")
    if ans == 1:
        return order, client_sum, holder_sum
    else:
        return "Error", 0, 0



@router.callback_query(Text(startswith="pp_"))
async def choose_pp_actions(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")

    if action[1] == 'show':
        pass
    elif action[1] == 'new':
        await callback.message.answer(
            f"Введите дату ПП или выберите:", reply_markup=pp_inline_kb.newPP_choose_date() 
        )
        await state.set_state(PPWork.new_pp_date)
    elif action[1] == 'exit':
        await callback.message.answer(
            f"Отмена ввода нового ПП. Выберите следущее действие:", reply_markup=pp_inline_kb.get_pp_kb()   
        )
    

@router.message(PPWork.new_pp_date)
async def pp_new_enter_date(message: Message, state: FSMContext):
    
    print(message.text.format())
    await state.update_data(pp_date=message.text.lower())
    tx = await state.get_data()
    print(tx)
    await message.answer(
        text="Теперь, пожалуйста, введите номер ПП:",
        input_field_placeholder="Номер ПП"
    )
    await state.set_state(PPWork.new_pp_number)

@router.callback_query(PPWork.new_pp_date, Text(startswith="PP_date_"))
async def pp_new_choosen_date(callback: types.CallbackQuery, state: FSMContext):
    
    print(callback.data.format())
    await state.update_data(pp_date=callback.data.split("_")[2])
    
    tx = await state.get_data()
    print(tx)
    await callback.message.answer(
        text="Теперь, пожалуйста, введите номер ПП:",
        input_field_placeholder="Номер ПП"
    )
    await state.set_state(PPWork.new_pp_number)



@router.message(PPWork.new_pp_number)
async def pp_new_enter_number(message: Message, state: FSMContext):
    await state.update_data(pp_number=message.text.lower())
    print(message.text.format())
    #clients_list = 
    await message.answer(
        f"Выберите клиента:", reply_markup=pp_inline_kb.get_pp_clients(db_bank.get_clients_list())
    )
    await state.set_state(PPWork.choose_client)


@router.callback_query(PPWork.choose_client, Text(startswith="PP_client_"))
async def pp_new_choosen_client(callback: types.CallbackQuery, state: FSMContext):
    
    await state.update_data(pp_client=callback.data.split("_")[2])
    tx = await state.get_data()
    print(tx)
    await callback.message.answer(
        text="Теперь, пожалуйста, выберите банк:", reply_markup=pp_inline_kb.get_pp_banks(db_bank.get_banks_list("'IP'"))
    )
    await state.set_state(PPWork.choose_bank)


@router.callback_query(PPWork.choose_bank, Text(startswith="PP_bank_"))
async def pp_new_choosen_bank(callback: types.CallbackQuery, state: FSMContext):
    
    print(callback.data.split("_")[2])
    await state.update_data(pp_bank=callback.data.split("_")[2])
    
    tx = await state.get_data()
    print(tx)
    await callback.message.answer(
        text="Теперь, пожалуйста, выберите держателя:",  reply_markup=pp_inline_kb.get_pp_holders(db_bank.get_name_holders("'IP'"))
    )
    await state.set_state(PPWork.choose_holder)


@router.callback_query(PPWork.choose_holder, Text(startswith="PP_holder_"))
async def pp_new_choosen_holder(callback: types.CallbackQuery, state: FSMContext):
    
    print(callback.data.split("_")[2])
    await state.update_data(pp_holder=callback.data.split("_")[2])
    
    tx = await state.get_data()
    print(tx)
    await callback.message.answer(
        text="Теперь, пожалуйста, введите сумму ПП:"
    )
    await state.set_state(PPWork.new_pp_sum)


@router.message(PPWork.new_pp_sum)
async def pp_new_enter_sum(message: Message, state: FSMContext):
    await state.update_data(pp_sum=message.text.lower())
    print(message.text.format())
    
    await message.answer(
        f"По умолчанию, процент банка устанволен 1%. Хотите изменить?:", reply_markup=pp_inline_kb.choose_tariff()
    )
    await state.set_state(PPWork.new_pp_tariff)


@router.callback_query(PPWork.new_pp_tariff, Text(startswith="PP_tariff_"))
async def pp_new_choose_tariff(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split("_")[2])

    if callback.data.split("_")[2] == "no":
        await state.update_data(pp_tariff=0.01)
        await callback.message.answer(
        f"Процент банка устанволен 1% ! Дополнительный процент, по умолчанию установлен 1%. Хотите изменить?:", reply_markup=pp_inline_kb.choose_add_tariff()
    )
        await state.set_state(PPWork.new_pp_add_tariff)
    elif callback.data.split("_")[2] == "yes":
         await callback.message.answer(text="Теперь, пожалуйста, введите процент банка, в формате 1 = 1% :"
    )

@router.message(PPWork.new_pp_tariff)
async def pp_new_enter_tariff(message: Message, state: FSMContext):
    await state.update_data(pp_tariff=float(message.text.lower())/100)
    print(message.text.format())
    tx = await state.get_data()
    print(tx)
    await message.answer(
        text=f"Банковский процент ={tx['pp_tariff']} \nДополнительный процент, по умолчанию установлен 1%. Хотите изменить?:", 
        reply_markup=pp_inline_kb.choose_add_tariff()
    )
    await state.set_state(PPWork.new_pp_add_tariff)


@router.callback_query(PPWork.new_pp_add_tariff, Text(startswith="PP_addtariff_"))
async def pp_new_choose_add_tariff(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split("_")[2])

    if callback.data.split("_")[2] == "no":
        await state.update_data(pp_add_tariff=0.01)
        await callback.message.answer(
        f"Дополнительный процент банка устанволен 1%!"
        )
        tx = await state.get_data()
        order, client_sum, holder_sum = write_new_order(tx)

        if order == "Error":
            await callback.message.answer(
                text=f"Ошибка записи! Попробовать еще раз?", reply_markup=pp_inline_kb.choose_next_new_order()
            )
            await state.clear()
        
        else:
            await callback.message.answer(
                text=f"Запись прошла успешно!\nЖелаете добавить еще ПП?", reply_markup=pp_inline_kb.choose_next_new_order()
        
            )
            await state.clear()

    elif callback.data.split("_")[2] == "yes":
        await callback.message.answer(text="Теперь, пожалуйста, введите дополнительный процент, в формате 1 = 1% :"
        )


@router.message(PPWork.new_pp_add_tariff)
async def pp_new_enter_add_tariff(message: Message, state: FSMContext):
    await state.update_data(pp_add_tariff=float(message.text.lower())/100)
    
    tx = await state.get_data()
    await message.answer(
        text=f"Дополнительный процент установлен {tx['pp_add_tariff']}%!"
    )
    order, client_sum, holder_sum = write_new_order(tx)

    if order == "Error":
        await message.answer(
            text=f"Ошибка записи! Попробовать еще раз?", reply_markup=pp_inline_kb.choose_next_new_order()
        )
        await state.clear()
    
    else:
        await message.answer(
            text=f"Запись прошла успешно!\nЖелаете добавить еще ПП?", reply_markup=pp_inline_kb.choose_next_new_order()
        )
        await state.clear()
    