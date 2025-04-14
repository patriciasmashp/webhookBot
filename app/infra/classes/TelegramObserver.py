from typing import Callable
from infra.IFaces.IHandler import IHandler
from infra.IFaces.IRouter import IRouter
from infra.IFaces.ITelegramObserver import ITelegramObserver
from infra.classes.Handler import Handler
from schemas.TelegramModels import Update


class TelegramObserver(ITelegramObserver):

    handler: IHandler = None
    filter: Callable = None

    _router: IRouter = None

    def __init__(self, router: IRouter, event: str):
        self._router = router
        self.event = event

    def __call__(self, filter):
        observer = TelegramObserver(self._router, self.event)
        observer.filter = filter
        self._router.observers.append(observer)

        def wrapper(callback):
            handler = Handler(callback, filter)
            observer.handler = handler

            return callback

        return wrapper

    def triger(self, update):
        event = update.get_event_by_name(self.event)
        return self.handler(event)

    def check(self, update: Update):
        try:
            update_dict = update.model_dump()
            if update_dict[self.event]:
                event = update.get_event_by_name(self.event)
                return self.filter(event)
        except Exception:
            return False
