from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from celery import shared_task

from aiogram import Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.filters.states import Registration
from app.users.models import TelegramUser
from bot.utils.kbs import contact_kb, language_kb
from bot.utils.storage import DjangoRedisStorage

User = get_user_model()


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


async def return_hello():
    bot_session = AiohttpSession()
    bot = Bot(settings.BOT_TOKEN, parse_mode='HTML', session=bot_session)
    current_time = timezone.now()
    lang = TelegramUser.objects.filter(language__isnull=True)
    phone = TelegramUser.objects.filter(phone__isnull=True)
    fullname = TelegramUser.objects.filter(fullname__isnull=True)
    all_active_users = lang | phone | fullname
    all_active_users = all_active_users.filter(
        is_active=True).filter(updated_at__lt=current_time - timezone.timedelta(hours=1))
    async for user in all_active_users:
        storage_key = StorageKey(
            user_id=user.id,
            chat_id=user.id,
            bot_id=bot.id,
            destiny='default'
        )
        state = FSMContext(DjangoRedisStorage(bot),
                           key=storage_key)
        try:
            if not user.language:
                await state.set_state(Registration.language)
                await bot.send_message(user.id,
                                       str(_("Завершите регистрацию, чтобы участвовать в розыгрыше. \n"
                                             "Это займет всего несколько минут.")),
                                       reply_markup=language_kb())
            elif not user.fullname:
                await state.set_state(Registration.fio)
                await bot.send_message(user.id,
                                       str(_("Вы забыли указать Ваше имя! \n"
                                             "Пожалуйста, заполните его для продолжения регистрации.")),
                                       reply_markup=ReplyKeyboardRemove())
            elif not user.phone:
                await state.set_state(Registration.phone)
                await bot.send_message(user.id,
                                       str(_("Остался всего один шаг! \n"
                                             "Введите номер телефона, чтобы завершить регистрацию и ввести "
                                             "промо-код для участия в розыгрыше.")),
                                       reply_markup=contact_kb())
        except TelegramForbiddenError:
            user.is_active = False
            await user.asave()
    await bot.session.close()
    return 'hello'


@shared_task()
def sync_task():
    async_to_sync(return_hello)()
