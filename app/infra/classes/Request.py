import aiohttp


class Request:
    """Базовый класс запроса
    """

    def __init__(self, method: str, data: dict = {}):
        self.data = data
        self.method = method

    async def send(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.request(self.method, url,
                                       data=self.data) as resp:
                return await resp.json()
