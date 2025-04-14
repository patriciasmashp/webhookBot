from service.schemas.Post import Post
from .Base import Base
from sqlalchemy.orm import mapped_column, Mapped


class PostDBModel(Base):

    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True, name="id")
    body: Mapped[str]
    title: Mapped[str] = mapped_column(index=True)
    user_id: Mapped[int]

    def __init__(self, model: Post, **kw):
        
        self.id = model.id
        self.title = model.title
        self.body = model.body
        self.user_id = model.user_id
        # super().__init__(**kw)
