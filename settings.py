import pathlib

from pydantic import BaseSettings, conint, constr
from pydantic.validators import IPv4Address


class Settings(BaseSettings):
    DEBUG: bool = True

    DEVELOPER_NAME: constr(min_length=1, max_length=255) = 'Timur Polishchuk'
    DEVELOPER_URL: constr(min_length=1, max_length=255) = 'https://t.me/timur_polishchuk_official'
    DEVELOPER_EMAIL: constr(min_length=1, max_length=255) = 'timur.polishchuk.official@gmail.com'

    APP_HOST: constr(min_length=1, max_length=15) = str(IPv4Address('127.0.0.1' if DEBUG else '0.0.0.0'))
    APP_PORT: conint(ge=0) = 5000
    APP_PATH: constr(min_length=1, max_length=255) = f'{pathlib.Path(__file__).parent.resolve()}'

    REDIS_HOST: constr(min_length=1, max_length=255) = 'localhost'
    REDIS_PORT: conint(ge=0) = 6379
    JSON_RPC: constr(min_length=1, max_length=255) = '2.0'

    TEST_REQUEST_QUEUE: constr(min_length=1, max_length=255) = 'TEST_REQUEST_QUEUE'
