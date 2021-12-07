from typing import Optional, Tuple

from asyncpg.exceptions import UniqueViolationError

from .db_service import DBConnectionContext
from .exceptions import SameIdempRequest, UnexpectedFetchProblem, AccountNotExist, NotEnoughMoney, NoIdempKey


async def peer_balance(user_id: str, amount: int, idempotency_key: Optional[str]):
    if not idempotency_key:
        raise NoIdempKey

    async with DBConnectionContext() as conn:
        trans = conn.transaction()  # ¯\_(ツ)_/¯
        try:
            await trans.start()
            try:
                await conn.fetch(
                    f'''INSERT INTO paymentKey (userId, externalKey) VALUES ('{user_id}', '{idempotency_key}')'''
                )
            except UniqueViolationError as exc:
                raise SameIdempRequest
            except Exception as exc:
                raise UnexpectedFetchProblem from exc

            await check_current_balance(conn, user_id, amount)

            await conn.fetch(
                f'''INSERT INTO customer (userId, balance) VALUES ('{user_id}', {amount})
                ON CONFLICT (userId) DO UPDATE SET balance = customer.balance + {amount}
                '''
            )
        except Exception as exc:
            await trans.rollback()
            raise exc

        else:
            await trans.commit()


async def check_current_balance(conn, user_id: str, amount: int) -> None:
    if amount < 0:
        fetch_result = await conn.fetchrow(f'''SELECT balance FROM customer WHERE userid = '{user_id}\'''')
        if not fetch_result:
            raise AccountNotExist

        current_balance = fetch_result['balance']
        to_be = current_balance + amount
        if to_be < 0:
            raise NotEnoughMoney
