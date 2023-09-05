from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove



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

    lk_menu = State()
    lk_choose_holders = State()
    lk_choose_banks = State()
