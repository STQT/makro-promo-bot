from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.utils.translation import gettext_lazy as _
from aiogram.types import KeyboardButton, ReplyKeyboardRemove

from bot.filters.states import Registration
from app.users.models import TelegramUser as User
from bot.functions import send_registered_message
from bot.validators import validate_code

router = Router()

languages = ("Ozbek tili", "Русский язык")


@router.message(Command("start"))
async def on_start(message: types.Message, command: CommandObject, state: FSMContext, user: User):
    promo = None
    if command.args:
        promo = command.args
        if validate_code(message, promo) is False:
            await message.answer(str(_("Ваш промокод неверный! Сканируйте верный QR-код")))
            return
    hello_text = ("Вас приветствует бот акции «Купите Vida, выиграйте путевку в Каппадокию!»\n"
                  "Этот бот поможет Вам в регистрации промо-кодов для участия в розыгрыше!\n"
                  "Пожалуйста, выберите язык\n\n"
                  "“Vida xarid qiling, Kapadokyaga sayohat yutib oling!” aksiyasi botiga xush kelibsiz.\n"
                  "Ushbu bot sizga o‘yinda ishtirok etish uchun promo-kodlarni ro‘yxatdan o‘tkazishda yordam beradi!\n"
                  "Iltimos, tilni tanlang")
    markup = ReplyKeyboardBuilder()
    markup.add(
        *(KeyboardButton(text=lang) for lang in languages)
    )
    if not user.language or not user.phone or not user.fullname:
        await message.answer(hello_text, reply_markup=markup.adjust(2).as_markup(resize_keyboard=True))
        await state.set_state(Registration.language)
        await state.set_data({"promo": promo})
    else:
        await message.answer(str(_("Вы можете выбрать что-то!")))  # TODO: add replymarkup for menu buttons


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
                         reply_markup=markup.adjust(2).as_markup(resize_keyboard=True))
    await state.set_state(Registration.phone)


@router.message(Registration.phone)
async def registration_finish(message: types.Message, state: FSMContext, user: User):
    user.phone = message.contact.phone_number
    await user.asave()
    data = await state.get_data()
    promo = data.get("promo")
    if promo is None:
        await message.answer(
            str(_("Вы успешно зарегистрировались в платформе! Отправьте промокод сюда чтобы зарегистрировать его")),
            reply_markup=ReplyKeyboardRemove())
    else:
        await send_registered_message(message, promo)
    await state.clear()
