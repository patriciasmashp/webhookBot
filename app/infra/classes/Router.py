from typing import List
from infra.IFaces.ITelegramObserver import ITelegramObserver
from infra.IFaces.IRouter import IRouter
from infra.classes.TelegramObserver import TelegramObserver


class Router(IRouter):

    observers: List[ITelegramObserver] = []

    def __init__(self, name=None):
        self.name = name or str(id(self))
        self.message = TelegramObserver(self, event="message")
        self.callback_query = TelegramObserver(self, event="callback_query")
