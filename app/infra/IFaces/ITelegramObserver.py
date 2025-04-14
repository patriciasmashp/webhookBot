from infra.IFaces.IHandler import IHandler
from abc import ABC, abstractmethod


class ITelegramObserver(ABC):
    """Класс наблюдателя за событиями телеграмма

    Args:
        ABC (_type_): _description_
    """
    handler: IHandler = None

    @abstractmethod
    def __call__(self, filter):

        pass

    @abstractmethod
    def check():
        """Проверка соответсвия события хэндлдеру
        """
        pass
    
    @abstractmethod
    def triger(self) -> IHandler:
        """Запуск обработчика события

        Returns:
            IHandler:
        """
        pass