from django.utils.translation import gettext_lazy as _


async def register_promo(code, user_id):
    return code


async def send_registered_message(message, promo):
    await register_promo(promo, message.from_user.id)
    await message.answer(
        str(_("Ваш промокод успешно зарегистрирован!"))  # TODO: add replymarkup for menu buttons
    )
