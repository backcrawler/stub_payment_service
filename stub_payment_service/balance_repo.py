from typing import Optional, Tuple

from asyncpg.exceptions import UniqueViolationError

from .db_service import DBConnectionContext


async def peer_balance(user_id: str, amount: int, idempotency_key: Optional[str]):
    if not idempotency_key:
        return {'result': 'failed', 'reason': 'no idempotency key provided'}

    try:
        async with DBConnectionContext() as conn:
            trans = conn.transaction()  # ¯\_(ツ)_/¯
            try:
                try:
                    await conn.fetch(
                        f'''INSERT INTO paymentKey (userId, externalKey) VALUES ('{user_id}', '{idempotency_key}')'''
                    )
                except UniqueViolationError as exc:
                    print(f'Index error occurred: {exc}; {type(exc)}')
                    return {'result': 'success'}
                except Exception as exc:
                    print(f'Error occurred: {exc}')
                    # await trans.rollback()
                    return {'result': 'failed', 'reason': 'internal error'}

                check_status, return_result = await check_current_balance(conn, user_id, amount)
                if not check_status:
                    return return_result

                await conn.fetch(
                    f'''INSERT INTO customer (userId, balance) VALUES ('{user_id}', {amount})
                    ON CONFLICT (userId) DO UPDATE SET balance = customer.balance + {amount}
                    '''
                )
            except Exception as exc:
                await trans.rollback()
                raise exc

    except Exception as exc:
        print(f'Error occurred: {exc}')
        return {'result': 'failed', 'reason': 'internal error'}

    else:
        return {'result': 'success'}


async def check_current_balance(conn, user_id: str, amount: int) -> Tuple[bool, Optional[dict]]:
    if amount < 0:
        fetch_result = await conn.fetchrow(f'''SELECT balance FROM customer WHERE userid = '{user_id}\'''')
        if not fetch_result:
            return False, {'result': 'failed', 'reason': 'account does not exist'}  # todo: change

        current_balance = fetch_result['balance']
        to_be = current_balance + amount
        if to_be < 0:
            return False, {'result': 'failed', 'reason': 'not enough money'}

    return True, None
