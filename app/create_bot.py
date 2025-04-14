from config import config
from infra.IFaces.IBot import IBot
from infra.classes.Bot import Bot

bot: IBot = Bot(config.token)
