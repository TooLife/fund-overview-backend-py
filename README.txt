基金管理系统
===========

一个基于 FastAPI 和 Redis 的基金管理系统，提供基金信息管理和实时估值查询功能。

项目结构
-------
.
├── app/
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置文件
│   ├── models/
│   │   └── fund.py         # 数据模型
│   ├── services/
│   │   ├── fund_service.py    # 基金服务
│   │   └── estimation_service.py  # 估值服务
│   └── api/
│       └── fund_api.py     # API路由
└── requirements.txt         # 项目依赖

安装依赖
-------
pip install -r requirements.txt

运行服务
-------
uvicorn app.main:app --reload

API 文档
-------

基础信息:
- 基础路径: /api
- 响应格式: JSON

接口列表:

1. 获取所有基金
---------------
获取系统中所有基金的信息列表。

路径: /funds
方法: GET
响应示例:
{
    "funds": [
        {
            "code": "161725",
            "name": "招商中证白酒指数(LOF)A",
            "currentPrice": "45.67",
            "profit": "1,250.00",
            "totalCost": "10,000.00",
            "fundRecords": [...]
        }
    ]
}

2. 获取单个基金
---------------
获取指定基金代码的详细信息。

路径: /funds/{code}
方法: GET
参数: 
  - code: 基金代码（路径参数）
响应示例:
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
        }
    ]
}

3. 创建基金
-----------
创建新的基金记录。

路径: /funds
方法: POST
请求体:
{
    "code": "161725",
    "name": "招商中证白酒指数(LOF)A",
    "currentPrice": "45.67",
    "profit": "1,250.00",
    "totalCost": "10,000.00",
    "fundRecords": []
}
响应: 返回创建的基金信息

4. 更新基金
-----------
更新指定基金的信息。

路径: /funds/{code}
方法: PUT
参数: 
  - code: 基金代码（路径参数）
请求体: 同创建基金
响应: 返回更新后的基金信息

5. 删除基金
-----------
删除指定的基金记录。

路径: /funds/{code}
方法: DELETE
参数: 
  - code: 基金代码（路径参数）
响应示例:
{
    "message": "删除成功"
}

6. 获取基金估值
--------------
获取基金的实时估值信息。

路径: /funds/{code}/estimation
方法: GET
参数: 
  - code: 基金代码（路径参数）
  - force_refresh: 是否强制刷新缓存（可选，默认false）
响应示例:
{
    "code": "161725",
    "name": "招商中证白酒指数(LOF)A",
    "currentPrice": "0.8334",
    "time": "2024-03-21 15:00",
    "cached": false
}

错误响应
-------
所有接口在发生错误时会返回统一格式的错误信息：

{
    "detail": "错误信息描述"
}

常见错误状态码：
- 400: 请求参数错误（如基金代码已存在）
- 404: 资源不存在（如基金不存在）
- 408: 请求超时
- 500: 服务器内部错误

数据模型
-------

Fund（基金）:
{
    "code": "string",      // 基金代码
    "name": "string",      // 基金名称
    "currentPrice": "string", // 当前价格
    "profit": "string",    // 收益
    "totalCost": "string", // 总成本
    "fundRecords": []      // 交易记录列表
}

FundRecord（交易记录）:
{
    "date": "string",    // 交易日期
    "amount": "string",  // 交易金额
    "price": "string",   // 交易价格
    "shares": "string",  // 份额
    "rate": "string",    // 费率
    "profit": "string",  // 收益
    "days": "string"     // 持有天数
}

开发环境要求
----------
- Python 3.8+
- Redis 5.0+
- FastAPI 0.115.12
- Uvicorn 0.34.0

数据初始化
---------
运行以下命令初始化示例数据：
python -m app.scripts.init_data

可选参数：
- --no-clear: 不清理现有数据
- --clear-only: 仅清理数据，不初始化

缓存说明
-------
- 基金估值数据默认缓存10秒
- 可通过 force_refresh 参数强制刷新缓存
- Redis 用于存储基金数据和缓存估值信息 