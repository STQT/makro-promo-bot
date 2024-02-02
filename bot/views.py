import asyncio
import json

from django.http import HttpResponse

from .misc import dp, bot


def process_update(request, token: str):
    if token == bot.token:
        body_unicode = request.body.decode('utf-8')
        update = json.loads(body_unicode)
        loop = asyncio.get_event_loop()
        loop.create_task(dp.feed_raw_update(bot, update))
        return HttpResponse(status=200)
    return HttpResponse(status=400)


process_update.csrf_exempt = True
