from typing import Optional

from fastapi import APIRouter, Header

from .exceptions import SameIdempRequest, AccountNotExist, NotEnoughMoney, NoIdempKey
from .schemas import BalanceChange
from .balance_repo import peer_balance

router = APIRouter()


@router.post('/top-up')
async def top_up_balance(balance: BalanceChange, idempotency_key: Optional[str] = Header(None)):
    try:
        await peer_balance(balance.user_id, balance.amount, idempotency_key)
    except SameIdempRequest:
        return {'result': 'success'}
    except NoIdempKey:
        return {'result': 'failed', 'reason': 'no idempotency key provided'}
    except AccountNotExist:
        return {'result': 'failed', 'reason': 'account does not exist'}
    except Exception as exc:
        return {'result': 'failed', 'reason': 'internal error'}
    else:
        return {'result': 'success'}


@router.post('/top-down')
async def top_down_balance(balance: BalanceChange, idempotency_key: Optional[str] = Header(None)):
    try:
        await peer_balance(balance.user_id, -balance.amount, idempotency_key)
    except SameIdempRequest:
        return {'result': 'success'}
    except AccountNotExist:
        return {'result': 'failed', 'reason': 'account does not exist'}
    except NoIdempKey:
        return {'result': 'failed', 'reason': 'no idempotency key provided'}
    except NotEnoughMoney:
        return {'result': 'failed', 'reason': 'not enough money'}
    except Exception as exc:
        return {'result': 'failed', 'reason': 'internal error'}
    else:
        return {'result': 'success'}
