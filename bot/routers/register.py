from datetime import date

from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.utils.translation import gettext_lazy as _
from aiogram.types import KeyboardButton, ReplyKeyboardRemove

from app.promotions.models import Promotion
from bot.filters.states import Registration
from app.users.models import TelegramUser as User
from bot.functions import send_registered_message
from bot.utils.contents import no_promo_code
from bot.utils.kbs import contact_kb, language_kb, languages, menu_kb

router = Router()


@router.message(Command("start"))
async def on_start(message: types.Message, command: CommandObject, state: FSMContext, user: User):
    promo = None
    if command.args:
        promo = command.args

    if not user.language or not user.phone or not user.fullname:
        today = date.today()
        today_promotion = await Promotion.objects.filter(
            start_date__lte=today, end_date__gte=today, is_active=True).afirst()
        description_ru = ""
        description_uz = ""
        if today_promotion:
            description_ru += today_promotion.description_ru
            description_uz += today_promotion.description_uz
            hello_text = (description_ru +
                          "\nПожалуйста, выберите язык\n\n" +
                          description_uz +
                          "\nIltimos, tilni tanlang")

            await message.answer(hello_text, reply_markup=language_kb())
            await state.set_state(Registration.language)
            await state.set_data({"promo": promo})
        else:
            await message.answer(no_promo_code)
    elif promo is not None:
        await send_registered_message(message, promo)
    else:
        await message.answer(str(_("Вы можете выбрать что-то!")), reply_markup=menu_kb())


@router.message(Registration.language)
async def registration_language(message: types.Message, state: FSMContext, user: User):
    if message.text and message.text in languages:
        user.language = 'uz' if message.text == languages[0] else 'ru'
        await user.asave()
        await state.set_state(Registration.fio)
        await message.answer(str(_("Пожалуйста, введите свое имя и фамилию.\n"
                                   "❗️Обращаем Ваше внимание – имя и фамилия должны соответствовать документам.")),
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(str(_("Неправильная команда")))


# @router.message(Command("registration"))
# async def start_register_user(message: types.Message, state: FSMContext):
#     await message.reply(str(_("Ismingizni kiriting:")))
#     await state.set_state(Registration.fio)
#     ...  # Register


@router.message(Registration.fio)
async def registration_phone(message: types.Message, state: FSMContext, user: User):
    user.fullname = message.text
    await user.asave()
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text=str(_("Отправить телефон")), request_contact=True))
    await message.answer(str(_("Введите Ваш контактный номер телефона регистрации промо-кода."
                               "В случае выигрыша приза, мы будем связываться с Вами по указанному номеру телефона.")),
                         reply_markup=contact_kb())
    await state.set_state(Registration.phone)


@router.message(Registration.phone)
async def registration_finish(message: types.Message, state: FSMContext, user: User):
    if message.contact:
        user.phone = message.contact.phone_number
        await user.asave()
        data = await state.get_data()
        promo = data.get("promo")
        if promo is None:
            await message.answer(
                str(_("Вы успешно зарегистрировались в платформе! Отправьте промокод сюда чтобы зарегистрировать его")),
                reply_markup=ReplyKeyboardRemove())  # TODO: need to change main menu buttons
        else:
            await send_registered_message(message, promo)
        await state.clear()
    else:
        await message.answer(str(_("Неправильно указан номер телефона. \n"
                                   "Пожалуйста, введите номер телефона в формате +998 хх ххх хх хх")),
                             reply_markup=contact_kb())
