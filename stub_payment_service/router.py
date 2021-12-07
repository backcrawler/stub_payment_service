from typing import Optional

from fastapi import APIRouter, Header

from .schemas import BalanceChange
from .balance_repo import peer_balance

router = APIRouter()


@router.post('/top-up')
async def top_up_balance(balance: BalanceChange, idempotency_key: Optional[str] = Header(None)):
    result = await peer_balance(balance.user_id, balance.amount, idempotency_key)
    return result


@router.post('/top-down')
async def top_down_balance(balance: BalanceChange, idempotency_key: Optional[str] = Header(None)):
    result = await peer_balance(balance.user_id, -balance.amount, idempotency_key)
    return result
