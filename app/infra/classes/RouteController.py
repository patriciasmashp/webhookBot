from typing import List
from schemas.TelegramModels import Update
from infra.IFaces.IRouter import IRouter
from infra.IFaces.ITelegramObserver import ITelegramObserver
from infra.classes.Base.Singleton import Singleton


class RouteController(Singleton):
    """Класс управления маршрутами
    Реализует паттерн Singleton
    Реализует паттерн Observer
    
    Регистрирует наблюдаетелй маршрутов и оповещает их при получении Update
    """
    _routers: List[IRouter] = []
    _hanlers: List[ITelegramObserver] = []

    def register_router(self, router: IRouter):
        """Регистрация маршрута

        Args:
            router (IRouter)
        """
        self._routers.append(router)
        self._hanlers.extend(router.observers)

    async def handle_update(self, update: Update):
        """Оповещение наблюдателей

        Args:
            update (Update): 

        Returns:
            IHandler: Обрабочтик события
        """

        for observer in self._hanlers:

            if observer.check(update):
                return await observer.triger(update)
