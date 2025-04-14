from typing import List
from service.IFaces.IWriter import IWriter
from service.PlaceHolderApi import PlaceHolderApi
from service.schemas.Post import Post


class Interactor:
    """Класс для взаимодействия с сервисами
    
    """
    writers: List[IWriter] = []

    def __init__(self, db_writer: IWriter, gs_writer: IWriter = None):
        self.writers.extend([db_writer])
        if gs_writer:
            self.writers.append(gs_writer)
        self.api = PlaceHolderApi()

    async def get_posts(self):
        """Метод получения списка постов

        Returns:
            List[Post]: Список Post
        """
        post = await self.api.get_posts()
        return post

    async def get_post(self, id: int):
        """Метод получения поста по id

        Args:
            id (int): id поста

        Returns:
            Post: Post
        
        """
        post = await self.api.get_post(id)
        await self._write(post)

        return post

    async def add_post(self, title: str, body: str, user_id: str):
        """Метод добавления поста

        Args:
            title (str): Заголовок поста
            body (str): Тело поста
            user_id (str): id пользователя

        Returns:
            Post: Post
        
        """
        post = Post(title=title, body=body, user_id=user_id)
        post = await self.api.add_post(post)
        await self._write(post)
        return post

    async def _write(self, data):
        """Метод записи данных в коллекции
        Todo:
            По хорошему избавится от IoBound и реализовать выполнение через фоновую задачу. Но я не успеваю до дедлайна

        Args:
            data (Post): Post
        
        """
        for writer in self.writers:
            await writer.write_post(data)
