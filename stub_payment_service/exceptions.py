class PaymentBaseException(Exception):
    """Must be inherited by all other custom Exception cases"""
    pass


class SameIdempRequest(PaymentBaseException):
    """Another request with same user_id/idempotency_key pair"""
    pass


class NoIdempKey(PaymentBaseException):
    """No idempotency_key provided"""
    pass


class UnexpectedFetchProblem(PaymentBaseException):
    """Unexpected problem while performing a db operation"""
    pass


class AccountNotExist(PaymentBaseException):
    """Account needs to be initialized before performing an operation"""
    pass


class NotEnoughMoney(PaymentBaseException):
    """Not enough money for such operation"""
    pass
