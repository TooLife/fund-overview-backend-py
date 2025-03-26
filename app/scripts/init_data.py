import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import redis
from app.services.fund_service import FundService
from app.models.fund import Fund, FundRecord
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

# 初始化数据
initial_data = {
    "funds": [
        {
            "code": "161725",
            "name": "招商中证白酒指数(LOF)A",
            "currentPrice": "45.67",
            "profit": "1,250.00",
            "totalCost": "10,000.00",
            "fundRecords": [
                {
                    "date": "2023-01-15",
                    "amount": "5,000.00",
                    "price": "50.00",
                    "shares": "100",
                    "rate": "5",
                    "profit": "250.00",
                    "days": "200"
                },
                {
                    "date": "2023-03-20",
                    "amount": "3,000.00",
                    "price": "30.00",
                    "shares": "100",
                    "rate": "3",
                    "profit": "90.00",
                    "days": "150"
                },
                {
                    "date": "2023-06-10",
                    "amount": "2,500.00",
                    "price": "25.00",
                    "shares": "100",
                    "rate": "2.5",
                    "profit": "62.50",
                    "days": "120"
                },
                {
                    "date": "2023-08-05",
                    "amount": "4,000.00",
                    "price": "40.00",
                    "shares": "100",
                    "rate": "4",
                    "profit": "160.00",
                    "days": "90"
                }
            ]
        },
        {
            "code": "g",
            "name": "黄金",
            "currentPrice": "45.67",
            "profit": "1,250.00",
            "totalCost": "10,000.00",
            "fundRecords": []
        }
    ]
}

def clear_all_data():
    """清理所有基金相关的数据"""
    print("开始清理数据...")
    
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )
    
    # 获取所有基金相关的键
    fund_keys = redis_client.keys("fund:*")
    if fund_keys:
        redis_client.delete(*fund_keys)
        print(f"已清理 {len(fund_keys)} 个基金相关的键")
    else:
        print("没有发现需要清理的数据")

def init_data(clear_existing: bool = True):
    """初始化基金数据
    
    Args:
        clear_existing: 是否清理现有数据，默认True
    """
    if clear_existing:
        clear_all_data()
    
    fund_service = FundService()
    print("\n开始初始化基金数据...")
    
    success_count = 0
    fail_count = 0
    
    for fund_data in initial_data["funds"]:
        try:
            # 创建Fund对象
            fund = Fund(**fund_data)
            # 调用创建接口
            fund_service.create_fund(fund)
            print(f"✓ 成功创建基金: {fund.code} - {fund.name}")
            success_count += 1
        except Exception as e:
            print(f"✗ 创建基金失败 {fund_data['code']}: {str(e)}")
            fail_count += 1
    
    print(f"\n数据初始化完成! 成功: {success_count}, 失败: {fail_count}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='初始化基金数据')
    parser.add_argument('--no-clear', action='store_true', help='不清理现有数据')
    parser.add_argument('--clear-only', action='store_true', help='仅清理数据，不初始化')
    
    args = parser.parse_args()
    
    if args.clear_only:
        clear_all_data()
    else:
        init_data(clear_existing=not args.no_clear) 