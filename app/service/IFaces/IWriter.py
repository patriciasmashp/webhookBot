from abc import ABC, abstractmethod

from service.schemas.Post import Post


class IWriter(ABC):
    """Интерфейс для записи постов
    """

    @abstractmethod
    async def write_post(self, post: Post):
        """Записать пост в коллекцию

        Args:
            post (Post): dto поста
        """
        pass
