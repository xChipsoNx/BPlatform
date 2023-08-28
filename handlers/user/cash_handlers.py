from aiogram import F, Router, types
from aiogram.types import Message 
from aiogram.filters import Command, Text
from aiogram import Router
from loader import db_bank
from utils.user_cls import User, Wallet, PP, Cash
from keyboards.inline.user_inline import holders_inline_kb, pp_inline_kb, cash_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import math, datetime

router = Router()


class CashStates(StatesGroup):
    cash_list = State()
    cash = State()

async def pp_info_show(callback,state):
    tx = await state.get_data()
    print(tx)
    pp = PP(*db_bank.get_pp_info_id(tx['order_id']))
    print(pp.get_list())
    
    payed = '❌' if pp.status == 'new' else '✅'


    info = f"""<i>Дата:</i> <b>{pp.date}</b> <i>Номер:</i> <b>{pp.number}</b> 
<i>Клиент:</i> <b>{pp.client_name}</b> <i>Дата закрытия:</i> <b>{pp.close_date}</b>
<i>Держатель:</i> <b>{pp.holder_name}</b> <i>Банк:</i> <b>{pp.bank_name}</b> 
<i>Сумма:</i> <b>{pp.sum}</b> <i>Налог:</i> <b>{pp.tax}</b> : <b>{payed}</b>
<i>Итог:</i> <b>{pp.total}</b> <i>Выплачено:</i> <b>{pp.close_sum}</b> 
    """

    await callback.message.answer(
        text=info,
        reply_markup=pp_inline_kb.pp_actions() 
    )





"""def write_new_order(pp):
    
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
    
    order = PP(None,pp['pp_date'], pp['pp_number'], client[1],wallet[1],wallet[0], sum, tariff, add_tariff, tax, total, 0, close_date, client[0],pp['pp_holder'],pp['pp_bank'], wallet[2],'new')
    
    ans = db_bank.add_new_order(order.get_list(), client_sum,holder_sum,"order")
    if ans == 1:
        return order, client_sum, holder_sum
    else:
        return "Error", 0, 0"""



@router.callback_query(Text(startswith="cash_"))
async def choose_cash_actions(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")

    if action[1] == 'task':
        task_list = db_bank.get_cash_list('task')
        await callback.message.answer(
            f"Выберите задание из списка:", reply_markup=cash_inline_kb.show_task_list(task_list, 0) 
        )
        await state.set_state(CashStates.cash_list)

    elif action[1] == 'show':
        await callback.message.answer(
            f"Введите дату ПП или выберите:", reply_markup=pp_inline_kb.newPP_choose_date() 
        )
        await state.set_state(CashStates.cash_list)

    elif action[1] == 'new':
        await callback.message.answer(
            f"Введите дату ПП или выберите:", reply_markup=pp_inline_kb.newPP_choose_date() 
        )
        await state.set_state(CashStates.cash_list)
    elif action[1] == 'exit':
        await callback.message.answer(
            f"Отмена ввода нового ПП. Выберите следущее действие:", reply_markup=pp_inline_kb.get_pp_kb()   
        )
    

"""@router.callback_query(PPWork.order, Text(startswith="PP_order_"))
async def pp_order(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split('_')
    tx = await state.get_data()

    if action[2] == 'page':
        pp_list = db_bank.get_pp_list()
        await callback.message.answer(
            f"Страница {int(action[3])+1}. Выберите ПП из списка:", 
            reply_markup=pp_inline_kb.show_pp_list(pp_list, int(action[3])) )
    elif action[2] == 'tax':
        #pp_list = db_bank.get_pp_list()
        tx = await state.get_data()
        print(tx['order_id'])
        db_bank.update_order_status(tx['order_id'],"tax_payed")
        await callback.message.answer(
            f"Налог оплачен."
            )
        await pp_info_show(callback, state)
    else:
        await state.update_data(order_id=action[2])
        await pp_info_show(callback, state)
    
    print(callback.data.format())



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
"""