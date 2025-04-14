from loguru import logger
from schemas.TelegramModels import Update
from aiohttp import web

from infra.classes.RouteController import RouteController


async def handler(request):
    data = await request.json()
    controller = RouteController()

    update = Update(**data)
    try:
        await controller.handle_update(update)
    except Exception as er:
        logger.exception(er)
        return web.Response(status=200)
    return web.Response(status=200)
