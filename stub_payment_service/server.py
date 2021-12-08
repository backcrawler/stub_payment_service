import time

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .configs.config import get_settings
from .router import router
from .db_service import DBConnectionContext
from .loggers import logger
from .utils import create_strict_periodic_task
# from .errors.error_handlers import http422_error_handler, http_error_handler, server_error_handler


def get_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name, debug=settings.debug, version=settings.version)

    application.add_event_handler("startup", set_periodic)

    # application.add_exception_handler(HTTPException, http_error_handler)
    # application.add_exception_handler(RequestValidationError, http422_error_handler)
    # application.add_exception_handler(Exception, server_error_handler)

    application.include_router(router)

    return application


def set_periodic() -> None:
    async def clear_payment_key_table():
        logger.info(f'Starting cleaning...')
        required_ts = int(time.time()) - 60  # 1 min
        async with DBConnectionContext() as conn:
            await conn.fetch(f'''DELETE FROM paymentKey WHERE createdTS < {required_ts}''')

    create_strict_periodic_task(clear_payment_key_table, 60*5, revokable=True)  # 5 minutes


# create app and serve forever with uvicorn
app = get_app()
