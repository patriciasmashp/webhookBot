from typing import List
from config import config
from service.BaseApi import BaseApi
from service.schemas.Post import Post


class PlaceHolderApi():
    """Класс для работы с API PlaceHolder"""

    def __init__(self):
        self.api_url = config.api_url

    async def get_posts(self) -> List[Post]:
        """Получение списка постов

        Returns:
            List[Post]: _description_
        """
        posts = await BaseApi.get(self.api_url + "/posts")
        return [Post.model_validate(post) for post in posts]

    async def get_post(self, id: int) -> Post:
        """Получение поста по id

        Args:
            id (int): id поста

        Returns:
            Post: DTO Поста
        """

        post = await BaseApi.get(self.api_url + "/posts/" + str(id))
        if post is None:
            raise Exception("Post not found")
        return Post.model_validate(post)

    async def add_post(self, post: Post) -> Post:
        """Добавление поста

        Args:
            post (Post): DTO Поста

        Returns:
            Post: DTO Поста
        """

        post = await BaseApi.post(self.api_url + "/posts", post.model_dump())
        return Post.model_validate(post)
