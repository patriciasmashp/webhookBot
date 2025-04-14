from urllib.parse import urlencode
import aiohttp
from loguru import logger
from pydantic import BaseModel


class BaseApi:
    "Базовый класс для работы с API"

    async def get(url: str,
                  params: dict | str | None = None,
                  headers: dict = None):
        """GET запрос

        Args:
            url (str): url запроса
            params (dict | str | None, optional): параметры запроса. Defaults to None.
            headers (dict, optional): заголовки запроса. Defaults to None.

        Returns:
            dict: ответ сервера
        """

        if type(params) is dict:
            params = urlencode(params)
        if params:
            url = url + "?" + params
        async with aiohttp.ClientSession() as session:

            async with session.get(url, headers=headers) as response:
                if response.ok:
                    succes = await response.json()
                    return succes
                else:
                    error = await response.json()
                    logger.error(error)
                    return None

    async def post(url: str,
                   data: dict | BaseModel,
                   params: dict | str = None,
                   headers: dict = None,
                   json: bool = True):
        if type(params) is dict:
            params = urlencode(params)
        if issubclass(data.__class__, BaseModel):
            data = data.model_dump()
        if params:
            url = url + "?" + params

        async with aiohttp.ClientSession() as session:
            if json:
                async with session.post(url, headers=headers,
                                        json=data) as response:
                    if response.ok:
                        succes = await response.json()
                        return succes
                    else:
                        errors = await response.read()
                        logger.exception(BaseException(errors))
                        return None
            else:
                async with session.post(url, headers=headers,
                                        data=data) as response:
                    if response.ok:
                        succes = await response.read()
                        return succes
                    else:
                        errors = await response.read()
                        logger.exception(errors)
                        return None

    async def put(url: str,
                  data: dict | BaseModel,
                  params: dict | str = None,
                  headers: dict = None):
        if type(params) is dict:
            params = urlencode(params)
        if issubclass(data.__class__, BaseModel):
            data = data.model_dump()
        if params:
            url = url + "?" + params
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers,
                                   json=data) as response:
                if response.ok:
                    succes = await response.json()
                    return succes
                else:
                    errors = await response.read()
                    logger.error(errors)
                    return None

    async def delete(url, params: dict = None, headers: dict = None):

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.ok:

                    return True
                else:
                    errors = await response.read()
                    logger.error(errors)
                    return None
