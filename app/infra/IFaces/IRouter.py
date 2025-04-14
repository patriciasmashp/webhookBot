from abc import ABC
from typing import List

from infra.IFaces.IHandler import IHandler
from infra.IFaces.ITelegramObserver import ITelegramObserver


class IRouter(ABC):
    """Класс контейнера для наблюдателей"""
    name: str
    observers: List[ITelegramObserver]
