from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == 'pars_all_product')
async def pars_all_product_functions(callback: CallbackQuery, state: FSMContext):
    pass