from fastapi import APIRouter, HTTPException
from typing import List

from ..models.fund import FundOverview, FundDetail, FundRecord
from ..services.estimation_service import EstimationService
from ..services.fund_service import FundService

router = APIRouter()
fund_service = FundService()
estimation_service = EstimationService()


@router.get("/funds/overview", response_model=List[FundOverview])
async def get_funds_overview():
    return fund_service.get_fund_overview()


@router.get("/funds/{code}/estimation")
async def get_fund_estimation(code: str, force_refresh: bool = False):
    """获取基金估值
    
    Args:
        code: 基金代码
        force_refresh: 是否强制刷新缓存，默认False
    """
    result = await estimation_service.get_fund_estimation(code, force_refresh)
    if result:
        fund_service.refresh_fund_price(code, result['currentPrice'])
    return result
