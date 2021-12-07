import uvicorn

from stub_payment_service.server import app
from stub_payment_service.configs.config import get_settings


if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run(app, host=settings.host, port=settings.port)
