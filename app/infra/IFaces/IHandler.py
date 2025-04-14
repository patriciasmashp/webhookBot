from abc import ABC, abstractmethod


class IHandler(ABC):
    _handler_filter = None

    @abstractmethod
    def __call__():
        pass
