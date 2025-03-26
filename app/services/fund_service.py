import json
from typing import Optional, List

import redis

from ..config import REDIS_HOST, REDIS_PORT, REDIS_DB
from ..models.fund import FundOverview, FundDetail, FundRecord


class FundService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

        # 键名前缀定义
        self.FUND_OVERVIEW_KEY_PREFIX = "fund:overview"  # Hash 纪录基金概览信息
        self.FUND_RECORDS_KEY_PREFIX = "fund:records:"  # 基金交易记录, fund:records:161725,List

    def _get_fund_records_key(self, code: str) -> str:
        return f"{self.FUND_RECORDS_KEY_PREFIX}{code}"

    def get_fund_overview(self) -> List[FundOverview]:
        """获取基金概览信息"""
        fund_overviews = []
        raw_fund_overviews = self.redis_client.hvals(self.FUND_OVERVIEW_KEY_PREFIX)
        for overview in raw_fund_overviews:
            fund_overviews.append(FundOverview(**json.loads(overview)))
        return fund_overviews

    def refresh_fund_price(self, code: str, curr_price: float):
        fund = self.redis_client.hget(self.FUND_OVERVIEW_KEY_PREFIX, code)
        if not fund:
            return
        fo = FundOverview(**json.loads(fund))
        fo.currentPrice = curr_price
        self.redis_client.hset(self.FUND_OVERVIEW_KEY_PREFIX, code, json.dumps(fo.dict()))
