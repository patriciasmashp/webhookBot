import inject
from loguru import logger
from infra.IFaces.IBot import IBot
from schemas.TelegramModels import CallbackQuery
from infra.classes.Bot import Bot
from infra.classes.Router import Router
from infra.classes.KeyBoardBuilder import InlineKeyBoardBuilder
from service.Interactor import Interactor
from service.PlaceHolderApi import PlaceHolderApi
from create_bot import bot

router = Router(name="action_router")


@router.callback_query(lambda callback_query: callback_query.data == "getall")
@inject.params(api=Interactor)
async def get_all(callback: CallbackQuery, api: Interactor = None):
    posts = await api.get_posts()
    kb = InlineKeyBoardBuilder()
    for post in posts[:4]:
        kb.add_inline_button(post.title, f"get_{post.id}")

    await bot.send_message(callback.message.chat.id,
                           "Список постов:",
                           reply_markup=kb.get_keyboard())


@router.callback_query(
    lambda callback_query: callback_query.data.startswith("get_"))
@inject.params(api=Interactor)
async def get_one(callback: CallbackQuery, api: Interactor = None):
    try:
        post = await api.get_post(callback.data.split("_")[1])
        await bot.send_message(callback.message.chat.id,
                               post.model_dump_json())
        await bot.send_alert(callback, "Данные сохранены")

    except Exception as e:
        logger.error(e)
        await bot.send_message(callback.message.chat.id, str(e))
