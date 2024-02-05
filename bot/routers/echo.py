from datetime import date

from aiogram import Router, types
from django.utils.translation import gettext_lazy as _, activate

from app.promotions.models import Promotion
from app.users.models import TelegramUser as User
from bot.functions import send_registered_message, get_all_user_promocodes
from bot.utils.kbs import menu_keyboards_dict
from bot.validators import validate_code

router = Router()


@router.message()
async def echo_handler(message: types.Message, user: User) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    menu_text_list = [menu for emoji_list in menu_keyboards_dict.values() for menu in emoji_list]
    activate(user.language)

    if message.text in menu_text_list:
        print(message.text in ("🆕 Ввод нового промо кода", "🆕 Yangi promokod kiritish"))
        if message.text in ("🆕 Ввод нового промо кода", "🆕 Yangi promokod kiritish"):
            await message.answer(str(_("Отправьте нам промокод")))
        elif message.text in ("💼 Мои промо коды", "💼 Promokodlarim"):
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
                    codes = str(_("Ваши промокоды: \n"))
                    codes += promo_codes_string
                    current_length = len(codes)

            if codes:
                await message.answer(codes)
            else:
                await message.answer(str(_("К сожалению, у Вас нет зарегистрированных промо кодов")))
        elif message.text in ("🌐 Социальные сети", "🌐 Ijtimoiy tarmoqlar"):
            socials = str(
                _("Наши социальные сети \n"
                  "<a href='https://google.com'>Фейсбук</a> | "
                  "<a href='https://google.com'>Инстаграм</a> | "
                  "<a href='https://google.com'>Телеграм</a>")
            )
            await message.answer(socials)
        elif message.text in ("🎁 Узнать текущую акцию", "🎁 Joriy aksiya bilan tanishish"):
            today = date.today()
            today_promotion = await Promotion.objects.filter(
                start_date__lte=today, end_date__gte=today, is_active=True).afirst()
            print(today_promotion)
            if today_promotion:
                await message.answer(today_promotion.name + "\n\n" + today_promotion.description)
            else:
                no_promo_code = str(_("Сейчас нет активных акций! "
                                      "Как только появится акция мы Вас обязательно уведомим"))
                await message.answer(no_promo_code)
        elif message.text in ("📜 Правила акции", "📜 Aksiya qoidalari"):
            rules = str(
                _(
                    "Правила использования платформы"
                )
            )
            await message.answer(rules)
        elif message.text in ("👤 Личный кабинет", "👤 Shaxsiy kabinet"):
            await message.answer(str(_(
                "<b>Полное имя:</b> {fullname}\n"
                "<b>Номер телефона:</b> {phone}").format(fullname=user.fullname, phone=user.phone)))
    else:
        if validate_code(message):
            await send_registered_message(message, message.text, user.language)
        else:
            await message.answer(str(_("Отправьте правильный промокод")))
