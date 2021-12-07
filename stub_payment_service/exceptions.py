class SameIdempRequest(Exception):
    """Another request with same user_id/idempotency_key pair"""
    pass


class NoIdempKey(Exception):
    """No idempotency_key provided"""
    pass


class UnexpectedFetchProblem(Exception):
    """Unexpected problem while performing a db operation"""
    pass


class AccountNotExist(Exception):
    """Account needs to be initialized before performing an operation"""
    pass


class NotEnoughMoney(Exception):
    """Not enough money for such operation"""
    pass
