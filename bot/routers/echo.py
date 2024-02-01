from datetime import date

from aiogram import Router, types
from django.utils.translation import gettext_lazy as _

from app.promotions.models import Promotion
from app.users.models import TelegramUser as User
from bot.functions import send_registered_message, get_all_user_promocodes
from bot.utils.contents import socials, rules, no_promo_code
from bot.utils.kbs import menu_keyboards_list
from bot.validators import validate_code

router = Router()


@router.message()
async def echo_handler(message: types.Message, user: User) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    if message.text in menu_keyboards_list:
        if message.text == _("🆕 Ввод нового промо кода"):
            await message.answer(str(_("Просто отправьте нам промокод")))
        elif message.text == _("💼 Мои промо коды"):
            codes = str(_("Ваши промокоды: \n"))
            db_codes = await get_all_user_promocodes(user)

            grouped_codes = {}
            for code in db_codes:
                timestamp = code.created_at.strftime('%d-%m-%Y %H:%M:%S')
                promotion_name = code.promotion.name
                if promotion_name not in grouped_codes:
                    grouped_codes[promotion_name] = []
                grouped_codes[promotion_name].append(f"{code.code} - {timestamp}")
            current_length = len(codes)

            for promotion_name, promo_codes in grouped_codes.items():
                promo_codes_string = f"{promotion_name}:\n"
                promo_codes_string += "\n".join(promo_codes)
                promo_codes_string += "\n\n"

                if current_length + len(promo_codes_string) < 1024:
                    codes += promo_codes_string
                    current_length += len(promo_codes_string)
                else:
                    await message.answer(codes)
                    codes = str(_("Your promo codes: \n"))
                    codes += promo_codes_string
                    current_length = len(codes)

            if codes:
                await message.answer(codes)
            else:
                await message.answer(str(_("К сожалению, у Вас нет зарегистрированных промо кодов")))
        elif message.text == _("🌐 Социальные сети"):
            await message.answer(socials)
        elif message.text == _("🎁 Узнать текущую акцию"):
            today = date.today()
            today_promotion = await Promotion.objects.filter(
                start_date__lte=today, end_date__gte=today, is_active=True).afirst()
            if today_promotion:
                await message.answer(today_promotion.name + "\n\n" + today_promotion.description)
            else:
                await message.answer(no_promo_code)
        elif message.text == _("📜 Правила акции"):
            await message.answer(rules)
        elif message.text == _("👤 Личный кабинет"):
            await message.answer(str(_(
                "<b>Полное имя:</b> {fullname}\n"
                "<b>Номер телефона:</b> {phone}").format(fullname=user.fullname, phone=user.phone)))
        else:
            if validate_code(message):
                await send_registered_message(message, message.text)
            else:
                await message.answer(str(_("Отправьте правильный промокод")))
