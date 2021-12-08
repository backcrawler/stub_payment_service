from typing import Callable, Awaitable, Any
import asyncio

from .loggers import logger


def create_strict_periodic_task(func: Callable, period: int, revokable=False) -> asyncio.Task:
    async def inner(f: Callable) -> None:
        while True:
            try:
                if asyncio.iscoroutinefunction(f):
                    await f()
                else:
                    f()
                await asyncio.sleep(period)
            except Exception as exc:
                if revokable:
                    logger.exception(f'Error while performing periodic task with {f.__name__} - {exc}')
                    await asyncio.sleep(5)
                else:
                    raise exc

    return asyncio.create_task(inner(func))


def create_adaptive_periodic_task(func: Callable[..., Awaitable[Any]], period: int, revokable=False) -> asyncio.Task:
    async def inner(f: Callable) -> None:
        while True:
            try:
                asyncio.create_task(f())
                await asyncio.sleep(period)
            except Exception as exc:
                if revokable:
                    logger.exception(f'Error while performing periodic task with {f.__name__} - {exc}')
                    await asyncio.sleep(5)
                else:
                    raise exc

    return asyncio.create_task(inner(func))

