import asyncio

from database.engine import create_db_and_tables, async_session
from handlers.main_handler import handler
from aiohttp import web
from loguru import logger
from config import config
from infra.classes.Request import Request
from infra.classes.Bot import Bot
from infra.classes.RouteController import RouteController
from infra.routes.StrartRouter import router as start_router
from infra.routes.ActionRoutes import router as action_router
from infra.routes.AddPostRouter import router as add_post_router
import inject
from create_bot import bot
from service.Interactor import Interactor
from service.PlaceHolderApi import PlaceHolderApi
from service.writers.DbWriter import DbWriter
from service.writers.GSheetsWriter import GSheetsWriter


def config_inject(binder):
    """Конфигурация инжектора

    Args:
        binder (_type_): _description_
    """
    binder.bind(Bot, bot)
    db_writer = DbWriter(async_session)
    try:
        gsheets_writer = GSheetsWriter(config.gsheet_creds_path,
                                       config.gsheets_token_path)
    except Exception as e:
        logger.error(e)
        gsheets_writer = None
    binder.bind(Interactor,
                Interactor(db_writer=db_writer, gs_writer=gsheets_writer))


async def on_strartup(app: web.Application):
    r = Request("GET")
    await create_db_and_tables()

    resp = await r.send(
        f"https://api.telegram.org:443/bot{config.token}/setWebhook?url={config.url}/api/v1"
    )
    logger.debug(resp)


async def on_shutdown(app: web.Application):
    r = Request("GET")
    resp = await r.send(
        f"https://api.telegram.org:443/bot{config.token}/deleteWebhook")
    logger.debug(resp)


async def init_app(loop):
    app = web.Application(middlewares=[])

    controller = RouteController()
    controller.register_router(start_router)
    controller.register_router(action_router)
    controller.register_router(add_post_router)
    app.router.add_post('/api/v1', handler)
    app.on_startup.append(on_strartup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        inject.configure(config_inject)
        app = loop.run_until_complete(init_app(loop))
        web.run_app(app, host=config.host, port=23456)
    except Exception as e:
        print('Error create server: %r' % e)
        logger.exception(e)

    finally:
        pass
    loop.close()
