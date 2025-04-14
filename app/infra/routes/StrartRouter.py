from create_bot import bot
from infra.classes.Router import Router
from infra.classes.KeyBoardBuilder import InlineKeyBoardBuilder
from schemas.TelegramModels import Message

router = Router(name="command_router")


@router.message(lambda message: message.text == "/start")
async def start(message: Message):
    builder = InlineKeyBoardBuilder()
    builder.add_inline_button("Получить посты", "getall")
    builder.add_inline_button("Добавить пост", "post")
    kb = builder.get_keyboard()

    await bot.send_message(message.chat.id,
                           "Выберите действие",
                           reply_markup=kb)
