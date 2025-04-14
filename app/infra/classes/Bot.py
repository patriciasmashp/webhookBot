from config import config
from schemas.TelegramModels import CallbackQuery, InlineKeyboardMarkup, MessageToSend
from infra.IFaces.IBot import IBot
from infra.classes.Request import Request


class Bot(IBot):
    """
    Класс для работы с Telegram Bot API
    Реализует Singleton 
    """

    token: str = None
    state = {}  # Словарь состояний
    _instance = None

    def __init__(self, token):
        self.token = token

    def __new__(class_, token, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    async def send_message(
        self,
        chat_id,
        text,
        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[])):
        """Метод отправки сообщения

        Args:
            chat_id (int): id пользователя tg
            text (str): текс сообщения
            reply_markup (InlineKeyboardMarkup, optional): Клавиатуры. Defaults to InlineKeyboardMarkup( inline_keyboard=[]).

        Raises:
            Exception: Ошибка отправки сообщения

        Returns:
            dict: Ответ telegram api
        """
        message = MessageToSend(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup.model_dump(exclude_none=True))
        r = Request("GET", message.model_dump(exclude_none=True))

        resp = await r.send(config.TG_API_URL + "/sendMessage")
        if resp["ok"]:

            return resp
        else:
            raise Exception(resp["description"])

    async def send_alert(self, callback_query: CallbackQuery, text):
        """Отправка  callback алерта

        Args:
            callback_query (CallbackQuery): callback
            text (_type_): текст алерта

        Raises:
            Exception: Ошибка отправки алерта

        Returns:
            dict: Ответ telegram api
        """
        r = Request(
            "GET", {
                "callback_query_id": callback_query.id,
                "text": text,
                "show_alert": False,
                "cache_time": 5
            })
        resp = await r.send(config.TG_API_URL + "/answerCallbackQuery")
        if resp["ok"]:
            return resp
        else:
            raise Exception(resp["description"])

    async def answer_callback_query(self, callback_query: CallbackQuery, text):
        r = Request("GET", {
            "callback_query_id": callback_query.id,
            "text": text
        })
        await r.send(config.TG_API_URL + "/answerCallbackQuery")
        await callback_query.answer(text)
