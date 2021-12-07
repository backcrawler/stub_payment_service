from pydantic import BaseModel, Field


class BalanceChange(BaseModel):
    user_id: str
    amount: int = Field(..., gt=0)
