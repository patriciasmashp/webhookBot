from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Post(BaseModel):
    """DTO поста"""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
    user_id: int
    id: int = Field(default=0)
    title: str
    body: str
