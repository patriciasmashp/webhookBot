import inject
from infra.IFaces.IBot import IBot
from schemas.TelegramModels import CallbackQuery, Message
from infra.classes.Bot import Bot
from infra.classes.Router import Router
from infra.classes.KeyBoardBuilder import InlineKeyBoardBuilder
from service.Interactor import Interactor
from service.PlaceHolderApi import PlaceHolderApi
from create_bot import bot

router = Router(name="action_router")


@router.callback_query(lambda callback_query: callback_query.data == "post")
@inject.params(api=Interactor)
async def post_name(callback: CallbackQuery, api: Interactor = None):
    text = "Название поста"
    bot.state[callback.message.chat.id] = {"user_id": callback.message.chat.id}
    await bot.send_message(callback.message.chat.id, text)


@router.message(lambda message: bot.state[message.chat.id]["title"])
@inject.params(api=Interactor)
async def post_add(message: Message, api: Interactor = None):
    bot.state[message.chat.id]["body"] = message.text
    post = await api.add_post(**bot.state[message.chat.id])
    bot.state[message.chat.id] = {}

    await bot.send_message(message.chat.id,
                           f"Пост добавлен:\n {post.model_dump_json()}")


@router.message(lambda message: bot.state[message.chat.id]["user_id"])
async def post_body(message: Message):
    bot.state[message.chat.id]["title"] = message.text
    await bot.send_message(message.chat.id, "Контент поста:")
