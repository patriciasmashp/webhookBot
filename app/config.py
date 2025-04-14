import json
import pathlib
from pydantic import Field
from pydantic_settings import BaseSettings
import os
import dotenv

dotenv.load_dotenv()


class Config(BaseSettings):
    db_url: str = "sqlite:///db.sqlite"
    token: str = os.environ["TOKEN"]
    host: str = os.environ.get("HOST", "0.0.0.0")
    TG_API_URL: str = Field(default_factory=lambda self:
                            'https://api.telegram.org/bot%s' % self['token'])
    api_url: str = "https://jsonplaceholder.typicode.com"
    url: str = os.environ["URL"]
    gsheet_creds_path: pathlib.Path = pathlib.Path(
        "gsheet_creds.json").absolute()
    gsheets_token_path: pathlib.Path = pathlib.Path("token.json").absolute()


config = Config()
