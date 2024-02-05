from dataclasses import dataclass
from datetime import date

from aiogram.types import Message, ReplyKeyboardRemove
from django.utils.translation import gettext_lazy as _
from app.promotions.models import Promotion, PromotionCode
from bot.utils.kbs import menu_kb
from bot.validators import validate_code
from app.users.models import TelegramUser as User


@dataclass
class RegisterPromo:
    CREATED = 1
    REGISTERED = 2
    ERROR = 3
    NO_PROMOTION = 4


async def register_promo(message, code):
    if validate_code(message, code):
        today = date.today()
        today_promotion = await Promotion.objects.filter(
            start_date__lte=today, end_date__gte=today, is_active=True).afirst()
        if today_promotion:
            promo, created = await PromotionCode.objects.aget_or_create(
                code=code,
                defaults={
                    "user_id": message.from_user.id,
                    "promotion": today_promotion})
            if created:
                return RegisterPromo.CREATED
            return RegisterPromo.REGISTERED
        return RegisterPromo.NO_PROMOTION
    return RegisterPromo.ERROR


async def send_registered_message(message: Message, promo, lang='ru'):
    created = await register_promo(message, promo)
    if created == RegisterPromo.CREATED:
        await message.answer(
            str(_("Ваш промокод успешно зарегистрирован!")),
            reply_markup=menu_kb(lang)
            # TODO: add replymarkup for menu buttons
        )
    elif created == RegisterPromo.REGISTERED:
        await message.answer(
            str(_("Ваш промокод уже имеется в нашей базе!")),
            reply_markup=menu_kb(lang)  # TODO: add replymarkup for menu buttons
        )
    elif created == RegisterPromo.ERROR:
        await message.answer(str(_("Неправильное значение промо кода. \n"
                                   "Пожалуйста, перепроверьте введенный промо-код и введите значение заново.")),
                             reply_markup=menu_kb(lang))
    else:
        await message.answer(str(_("Не найдена активная акция на сегодня")), reply_markup=menu_kb(lang))


async def get_all_user_promocodes(user: User):
    codes = []
    async for code in PromotionCode.objects.filter(user=user).select_related("promotion"):
        codes.append(code)
    return codes
