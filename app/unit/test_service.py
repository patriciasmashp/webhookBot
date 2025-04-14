import pytest
from service.schemas.Post import Post
from service.PlaceHolderApi import PlaceHolderApi
from service.Interactor import Interactor
from service.writers.DbWriter import DbWriter
from database.engine import async_session
from service.BaseApi import BaseApi
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_interactor_wrong_schema(monkeypatch):

    async def mock_get(*args, **kwargs):
        return {"mock_key": "mock_response"}

    monkeypatch.setattr(BaseApi, "get", mock_get)
    dbWriter = DbWriter(async_session)
    interactor = Interactor(dbWriter)
    with pytest.raises(ValidationError) as er:
        res = await interactor.get_post(1)


@pytest.mark.asyncio
async def test_interactor_wrong_id(monkeypatch):

    dbWriter = DbWriter(async_session)
    interactor = Interactor(dbWriter)
    with pytest.raises(Exception) as er:
        res = await interactor.get_post(1000000)

@pytest.mark.asyncio
async def test_interactor_get_post(monkeypatch):
    dbWriter = DbWriter(async_session)
    interactor = Interactor(dbWriter)
    
    res = await interactor.get_post(1)
    
    assert isinstance(res, Post)