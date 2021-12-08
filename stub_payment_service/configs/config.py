from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Payment Service'
    db_name: str
    db_host: str
    db_port: str
    db_password: str
    db_user: str
    debug: bool = True
    host: str
    log_lvl: str = 'INFO'
    port: int
    version: str = '0.0.1'

    class Config:
        env_file = './stub_payment_service/configs/.env'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
