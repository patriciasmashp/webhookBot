from abc import ABC, abstractmethod
from typing import Dict

user_id = str


class IBot(ABC):
    state: Dict[user_id, dict] = {}
    """словарь состояний"""

    @abstractmethod
    def send_message(self, chat_id, text, reply_markup):
        pass

    @abstractmethod
    def send_alert(self, callback_query, text):
        pass
