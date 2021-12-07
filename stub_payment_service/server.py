from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .configs.config import get_settings
from .router import router
# from .errors.error_handlers import http422_error_handler, http_error_handler, server_error_handler


def get_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name, debug=settings.debug, version=settings.version)

    # application.add_exception_handler(HTTPException, http_error_handler)
    # application.add_exception_handler(RequestValidationError, http422_error_handler)
    # application.add_exception_handler(Exception, server_error_handler)

    application.include_router(router)

    return application


# create app and serve forever with uvicorn
app = get_app()
