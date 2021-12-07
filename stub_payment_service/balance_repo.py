from typing import Optional

from asyncpg.exceptions import UniqueViolationError

from .db_service import get_db_connection


async def peer_balance(user_id: str, amount: int, idempotency_key: Optional[str]):
    if not idempotency_key:
        return {'result': 'failed', 'reason': 'no idempontency key provided'}

    conn = await get_db_connection()

    try:
        async with conn.transaction():
            try:
                await conn.fetch(
                    f'''INSERT INTO paymentKey (userId, externalKey) VALUES ('{user_id}', '{idempotency_key}')'''
                )
            except UniqueViolationError as exc:
                print(f'Index error occured: {exc}; {type(exc)}')
                return {'result': 'success'}  # todo: change
            except Exception as exc:
                print(f'Error occured: {exc}')
                return {'result': 'failed', 'reason': 'internal error'}

            if amount < 0:
                already_exists = await conn.fetch(f'''SELECT COUNT(*) FROM customer WHERE userid = '{user_id}\'''')
                if not already_exists:
                    print(f'Cannot withdrew with no account')
                    return {'result': 'failed', 'reason': 'account does not exist'}  # todo: change

            await conn.fetch(
                f'''INSERT INTO customer (userId, balance) VALUES ('{user_id}', {amount})
                ON CONFLICT (userId) DO UPDATE SET balance = customer.balance + {amount}
                '''
            )

    except Exception as exc:
        print(f'Error occured: {exc}')
        return {'result': 'failed', 'reason': 'internal error'}

    else:
        return {'result': 'success'}

    finally:
        await conn.close()
