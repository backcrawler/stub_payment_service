from pydantic import BaseModel, Field


class BalanceChange(BaseModel):
    user_id: str
    amount: int = Field(..., gt=0)


class MoneyExchange(BaseModel):
    payer_user_id: str
    payer_amount: int = Field(..., gt=0)
    buyer_user_id: str
