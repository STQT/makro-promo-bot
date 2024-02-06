from aiogram.types import Message

from app.promotions.models import Promotion


async def validate_code(message: Message, code: str = None):
    if code is None and message.text:
        code = message.text
    today_promotions = Promotion.objects.filter(is_active=True)
    promos = []
    async for promo in today_promotions:
        promos.append((promo.id, promo.mask))

    for promo_id, promo_mask in promos:
        if code.startswith(promo_mask):
            return True, promo_id
    return False, 0
