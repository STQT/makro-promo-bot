import random

from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.utils.translation import gettext_lazy as _, activate

from app.promotions.models import Promotion
from app.users.models import TelegramUser as User
from bot.functions import send_registered_message, get_all_user_promocodes
from bot.utils.kbs import menu_keyboards_dict
from bot.validators import validate_code

router = Router()


@router.callback_query(F.data.startswith("about_"))
async def get_about_id(callback: types.CallbackQuery):
    _about, promo_id = callback.data.split("about_")
    promotion = await Promotion.objects.filter(pk=promo_id).afirst()
    if promotion:
        await callback.answer(promotion.name)
        await callback.message.answer(promotion.conditions)
    else:
        await callback.answer(str(_("Отсутствует")))
    await callback.message.delete()
