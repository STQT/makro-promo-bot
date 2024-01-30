from aiogram.types import Message


def validate_code(message: Message, code: str = None):

    if message.text:
        if code is None:
            code = message.text

        ...  # TODO: check this code after
        if code == "test":
            return True
    return False
