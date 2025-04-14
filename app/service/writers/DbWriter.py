from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models.Post import PostDBModel
from service.IFaces.IWriter import IWriter
from service.schemas.Post import Post


class DbWriter(IWriter):

    def __init__(self, session_maker):
        self.session_maker: async_sessionmaker = session_maker

    async def write_post(self, data: Post):
        async with self.session_maker() as session:
            exist = await session.get(PostDBModel, data.id)
            if exist is None:

                post = PostDBModel(data)

                session.add(post)
                await session.commit()
