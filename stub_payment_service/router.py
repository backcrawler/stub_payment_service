import logging
from typing import Optional

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from .exceptions import SameIdempRequest, AccountNotExist, NotEnoughMoney, NoIdempKey
from .schemas import BalanceChange, MoneyExchange
from .balance_repo import peer_balance, exchange_balance

router = APIRouter()


@router.post('/top-up')
async def top_up_balance(balance_change: BalanceChange, idempotency_key: Optional[str] = Header(None)):  # todo: middleware
    try:
        await peer_balance(balance_change.user_id, balance_change.amount, idempotency_key)
    except SameIdempRequest:
        return JSONResponse(content={'result': 'success'}, status_code=200)
    except NoIdempKey:
        return JSONResponse(content={'result': 'failed', 'reason': 'no idempotency key provided'}, status_code=400)
    except AccountNotExist:
        return JSONResponse(content={'result': 'failed', 'reason': 'account does not exist'}, status_code=400)
    except Exception as exc:
        return JSONResponse(content={'result': 'failed', 'reason': 'internal error'}, status_code=500)
    else:
        return JSONResponse(content={'result': 'success'}, status_code=200)


@router.post('/top-down')
async def top_down_balance(balance_change: BalanceChange, idempotency_key: Optional[str] = Header(None)):
    try:
        await peer_balance(balance_change.user_id, -balance_change.amount, idempotency_key)
    except SameIdempRequest:
        return JSONResponse(content={'result': 'success'}, status_code=200)
    except NoIdempKey:
        return JSONResponse(content={'result': 'failed', 'reason': 'no idempotency key provided'}, status_code=400)
    except AccountNotExist:
        return JSONResponse(content={'result': 'failed', 'reason': 'account does not exist'}, status_code=400)
    except NotEnoughMoney:
        return JSONResponse(content={'result': 'failed', 'reason': 'not enough money'}, status_code=400)
    except Exception as exc:
        return JSONResponse(content={'result': 'failed', 'reason': 'internal error'}, status_code=500)
    else:
        return JSONResponse(content={'result': 'success'}, status_code=200)


@router.post('/exchange')
async def exchange_money(money: MoneyExchange, idempotency_key: Optional[str] = Header(None)):
    try:
        await exchange_balance(money.payer_user_id, money.payer_amount, money.buyer_user_id, idempotency_key)
    except SameIdempRequest:
        return JSONResponse(content={'result': 'success'}, status_code=200)
    except NoIdempKey:
        return JSONResponse(content={'result': 'failed', 'reason': 'no idempotency key provided'}, status_code=400)
    except AccountNotExist:
        return JSONResponse(content={'result': 'failed', 'reason': 'account does not exist'}, status_code=400)
    except NotEnoughMoney:
        return JSONResponse(content={'result': 'failed', 'reason': 'not enough money'}, status_code=400)
    except Exception as exc:
        logging.exception(f'EXC: {exc}')
        return JSONResponse(content={'result': 'failed', 'reason': 'internal error'}, status_code=500)
    else:
        return JSONResponse(content={'result': 'success'}, status_code=200)
