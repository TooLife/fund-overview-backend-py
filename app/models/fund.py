from typing import List

from pydantic import BaseModel


# FundRecord: 基金交易记录
class FundRecord(BaseModel):
    date: str
    amount: str
    price: str
    shares: str
    rate: str
    profit: str
    days: str


# FundOverview: 基金概览
class FundOverview(BaseModel):
    code: str
    name: str
    currentPrice: float = 0.0
    profit: float = 0.0
    totalCost: float = 0.0
    totalProfit: float = 0.0
    numOfTransactions: int = 0


# FundDetail: 基金详情
class FundDetail(BaseModel):
    code: str
    name: str
    currentPrice: str
    fundRecords: List[FundRecord]