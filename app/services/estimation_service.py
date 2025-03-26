import json
import random
import time

import redis
import requests
from fastapi import HTTPException

from ..config import USER_AGENTS, REDIS_HOST, REDIS_PORT, REDIS_DB, CACHE_EXPIRY


class EstimationService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

    async def get_fund_estimation(self, code: str, force_refresh: bool = False) -> dict:
        try:
            # 检查缓存
            cache_key = f"fund_estimation:{code}"
            if not force_refresh:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    data = json.loads(cached_data)
                    data['cached'] = True
                    return data

            # 获取实时数据
            time.sleep(random.uniform(0.1, 0.5))

            api_url = f"https://fundgz.1234567.com.cn/js/{code}.js"
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Referer': 'https://fund.eastmoney.com/',
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }

            response = requests.get(api_url, headers=headers, timeout=5)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="无法获取基金数据")

            response.encoding = 'utf-8'

            if not response.text.startswith('jsonpgz('):
                raise HTTPException(status_code=400, detail="数据格式错误")

            json_str = response.text[8:-2]
            data = json.loads(json_str)

            result = {
                "code": data["fundcode"],
                "name": data["name"],
                "currentPrice": float(data["gsz"]),
                "time": data["gztime"],
                "cached": False
            }

            # 保存到缓存
            self.redis_client.setex(
                cache_key,
                CACHE_EXPIRY,
                json.dumps(result)
            )

            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
