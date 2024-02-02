import asyncio
import json

from django.http import HttpResponse

from .misc import dp, bot


def process_update(request, token: str):
    if token == bot.token:
        body_unicode = request.body.decode('utf-8')
        update = json.loads(body_unicode)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the coroutine in the event loop
        loop.run_until_complete(dp.feed_raw_update(bot, update))

        # Close the event loop
        loop.close()
        return HttpResponse(status=200)
    return HttpResponse(status=400)


process_update.csrf_exempt = True
