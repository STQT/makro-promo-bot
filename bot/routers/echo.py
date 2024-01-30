from aiogram import Router, types
from django.utils.translation import gettext_lazy as _

from app.users.models import TelegramUser as User
from bot.functions import send_registered_message
from bot.validators import validate_code

router = Router()


@router.message()
async def echo_handler(message: types.Message, user: User) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    ...
    # TODO: check message.text to buttons
    print(message.bot.id)
    print(message.chat.id)
    print(message.from_user.id)
    if validate_code(message):
        await send_registered_message(message, message.text)
    else:
        await message.answer(str(_("Отправьте правильный промокод")))
