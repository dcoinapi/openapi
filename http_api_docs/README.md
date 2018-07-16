[[toc]]
#OpenApi
##说明

### 签名
请求参数按照字典排序，然后以keyvalue的形式拼接成字符串string，最后sign=MD5(string+secretKey)。注意：如果请求参数中value为NULL的
情况，则在拼接字符串时不计入签名字符串。
>例如：

参数如下：
```
{
    country = 86;
    mobile = 15882133579;
    password = 654321zz;
    time = 1516007245;
}
```
拼接完成后：

```
string = country86mobile15882133579password654321zztime1516007278
sign=MD5(string+secretKey)
```

### 请求格式
- post请求参数采用表单格式提交数据
content-type:application/x-www-form-urlencoded

- get请求格式如下：
http://192.168.50.27:7654/open/api/get_records?symbol=ltcbtc&period=10min

###返回格式
||**参数**|| **参数类型**||**必有**||**说明**||
||code||int||`true`||错误码，0为成功，其他失败||
||msg||string||`true`||错误信息||
||data||struct||flase||返回数据，具体见各请求||

##创建订单
`Post /open/api/create_order`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||side||string||`true`||买卖方向BUY,SELL||
||type||int||`true`||挂单类型，1:限价委托、2:市价委托||
||volume||float64||`true`||购买数量（多义，复用字段）<br>type=1:表示买卖数量<br>type=2:买则表示总价格，卖表示总个数||
||price||float64||false||委托单价：type=2：不需要此参数||
||symbol||string||`true`||市场标记，例：ethbtc||
||api_key||string||`true`||api_key||
||sign||string||`true`||签名||

>data说明
```json
"data": {	
	"order_id":创建的订单id
}
```
>返回示例
```json
{
    "code": 0,
    "msg": “success",
    "data": {
        "order_id": 954582
    }
}
```

##取消订单
`Post /open/api/cancel_order`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||order_id||int64||`true`||订单ID||
||symbol||string||`true`||市场标记，例：ethbtc||
||api_key||string||`true`||api_key||
||sign||string||`true`||签名||
>data说明

无data
<br>
>返回示例
```json
{
    "code": 0,
    "msg": "success",
    "data": null
}
```

##查询系统支持的所有交易对及精度
`Get /open/api/common/symbols`
<br>
>请求参数

无
<br>
>data说明
```json
"data": [
	{
		"symbol": 币对标识,
		"count_coin": 计量货币,
		"amount_precision":计量货币精度,
		"base_coin": 计价货币,
		"price_precision":计价货币精度
	}
]
```
>返回示例
```json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "symbol": "btcusdt",
            "count_coin": "btc",
            "amount_precision": 8,
            "base_coin": "usdt",
            "price_precision": 4
        },
        {
            "symbol": "ethusdt",
            "count_coin": "eth",
            "amount_precision": 4,
            "base_coin": "usdt",
            "price_precision": 4
        }
    ]
}
```

##获取用户已成交和已取消的委托
`Get /open/api/all_order`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
||pageSize||int||false||页面大小||
||page||int||false||页码||
||api_key||string||`true`||api_key||
||sign||string||`true`||签名||
>data说明
```
"data": {
	"count": 订单数量,
	"orderList": [
		{
			"id": 订单id,
			"side": 买卖方向,
			"symbol": 币对标识,
			"type": 订单类型，1定价 2市价,
			"price": 价格,
			"volume":数量,
			"status":订单状态 0初始，1新订单，2已成交，3部分成交，4已取消，5正在取消，6已过期,
			"deal_volume":已成交数量,
			"total_price":当前成交总价,
			"fee": 手续费,
			"age_price": 成交均价,
			"ts": 下单时间（ms时间戳）,
			"tradeList": [	订单成交记录,
				{
					"id":交易id,
					"price":成交价格,
					"volume":成交数量,
					"direction": 主动单方向,
					"ts": 成交时间
				}
			]
		}
	]
}
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "count": 310228,
        "orderList": [
            {
                "id": 954898,	
                "side": "BUY",		
                "symbol": "ltcbtc",		
                "type": 1,			
                "price": 0.01308999,	
                "volume": 0.099999,	
                "status": 4,
                "deal_volume": 0,	
                "total_price": 0,	
                "fee": 0,		
                "age_price": 0,		
                "ts": 152991761733,	
                "tradeList": []	
            },
            {
                "id": 954889,
                "side": "SELL",
                "symbol": "ltcbtc",
                "type": 1,
                "price": 0.01308799,
                "volume": 0.099999,
                "status": 2,
                "deal_volume": 0.099999,
                "total_price": 0.00130888591101,
                "fee": 0,
                "age_price": 0.01308899,
                "ts": 152991757143,
                "tradeList": [	
                    {
                        "id": 433425,	
                        "price": 0.01308899,	
                        "volume": 0.099999,	
                        "direction": "SELL",	
                        "ts": 152991757140	
                    }
                ]
            }
        ]
    }
}
```

##获取用户未成交或正在成交的委托
`Get /open/api/new_order`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
||pageSize||int||false||页面大小||
||page||int||false||页码||
||api_key||string||`true`||api_key||
||sign||string||`true`||签名||
>data说明

```json
"data": {
	"count": 订单数量,
	"orderList": [
		{
			"id": 订单id,
			"side": 买卖方向,
			"symbol": 币对标识,
			"type": 订单类型，1定价 2市价,
			"price": 价格,
			"volume":数量,
			"status":订单状态 0初始，1新订单，2已成交，3部分成交，4已取消，5正在取消，6已过期,
			"deal_volume":已成交数量,
			"total_price":当前成交总价,
			"fee": 手续费,
			"age_price": 成交均价,
			"ts": 下单时间（ms时间戳）,
			"tradeList": [	订单成交记录,
				{
					"id":交易id,
					"price":成交价格,
					"volume":成交数量,
					"direction": 主动单方向,
					"ts": 成交时间
				}
			]
		}
	]
}
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "count": 10,
        "orderList": [
            {
                "id": 955007,		
                "side": "SELL",		
                "symbol": "ltcbtc",		
                "type": 1,			
                "price": 0.01308099,	
                "volume": 0.099999,	
                "status": 1,	
                "deal_volume": 0,	
                "total_price": 0,		
                "fee": 0,		
                "age_price": 0,		
                "ts": 152991812844,	
                "tradeList": []		
            },
            {
                "id": 954889,
                "side": "SELL",
                "symbol": "ltcbtc",
                "type": 1,
                "price": 0.01308799,
                "volume": 0.199999,
                "status": 2,
                "deal_volume": 0.099999,
                "total_price": 0.00130888591101,
                "fee": 0,
                "age_price": 0.01308899,
                "ts": 152991757143,
                "tradeList": [
                    {
                        "id": 433425,		
                        "price": 0.01308899,	
                        "volume": 0.099999,	
                        "direction": "SELL",	
                        "ts": 152991757140	
                    }
                ]
            }
        ]
    }
}
```

##获取用户成交记录
`Get /open/api/all_trade`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
||pageSize||int||false||页面大小||
||page||int||false||页码||
||api_key||string||`true`||api_key||
||sign||string||`true`||签名||
>data说明

```json
"data": {
    "count": 293977,
    "resultList": [
        {
            "id": 交易id,
            "price": 成交价格,
            "volume": 成交数量,
            "direction": 主动单方向,
            "created_at": 成交时间
        }
    ]
}
```
>返回示例

```
{
    "code": 0,
    "msg": "success",
    "data": {
        "count": 293977,
        "resultList": [
            {
                "id": 294020,		
                "price": 0.01641,		
                "volume": 0.01,			
                "direction": "BUY",		
                "created_at": 152674785388	
            },
            {
                "id": 294019,
                "price": 0.016404,
                "volume": 0.01,
                "direction": "BUY",
                "created_at": 152674769427
            }
        ]
    }
}
```

##获取K线数据
`Get /open/api/get_records`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
||period||string||`true`||k线时间刻度，见下||
||size||int||false||请求出数据量，范围[1,2000] 默认150||

- period参数值
 1min
5min
15min
30min
60min
2hour
4hour
6hour
12hour
1day
1week
1month

>data说明

```json
"data": [
    {
        "id": k线id,
        "amount": 成交总价,
        "vol": 成交数量,
        "open": 开盘价格,
        "close": 收盘价格,
        "high": 最高价格,
        "low": 最低价格
    }
]
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 1529920380,		
            "amount": 10.21281696,	
            "vol": 1.2987000000000002,	
            "open": 7.8649,		
            "close": 7.8653,		
            "high": 7.8674,		
            "low": 7.8614		
        },
        {
            "id": 1529920440,
            "amount": 7.07179113,
            "vol": 0.8991,
            "open": 7.8641,
            "close": 7.8698,
            "high": 7.8698,
            "low": 7.862
        }
    ]
}
```

##获取当前行情
`Get /open/api/get_ticker`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
>data说明

```json
"data": {
    "time": 时间,
    "open": 24小时开盘价,
    "close":  24小时收盘价，即最新成交价,
    "high": 最高价,
    "low": 最低价,
    "vol": 成交量,
    "buy": [
        买一价,
        买一量
    ],
    "sell": [
        卖一价,
        卖一量
    ]
}
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "time": 1529920938122,		
        "open": "9.3090",		
        "close": "7.9059",		
        "high": "9.3090",			
        "low": "7.6399",		
        "vol": "37741.0180",		
        "buy": [
            "7.9017",			
            "0.0999"			
        ],
        "sell": [
            "7.9059",			
            "0.0999"			
        ]
    }
}
```

##获取行情成交记录
`Get /open/api/get_trades`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
||size||int||false||请求出数据量，范围[1,200] 默认100||
>data说明

```json
"data": [
    {
        "id": 交易id,
        "price": 成交价格,
        "volume": 成交数量,
        "direction": 主动单方向,
        "ts": 成交时间
    }
]
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 3103714,		
            "price": 7.8946,	
            "volume": 0.0999,		
            "direction": "SELL",		
            "ts": 1529921032304		
        },
        {
            "id": 3103713,
            "price": 7.8939,
            "volume": 0.0999,
            "direction": "SELL",
            "ts": 1529921029961
        },
        {
            "id": 3103712,
            "price": 7.8925,
            "volume": 0.0999,
            "direction": "SELL",
            "ts": 1529921027764
        }
    ]
}
```

##查询买卖盘深度
`Get /open/api/market_dept`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
||type||int||`true`||深度类型，step0, step1, step2（合并深度0-2）；step0时，精度最高||
>data说明

```json
"data": {
    "asks": [	卖盘
        [
            价格,
            数量
        ]
    ],
    "bids": [	卖盘
        [
            价格,
            数量
        ]
    ]
}
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "asks": [			
            [
                9.3119,		
                25.2012		
            ],
            [
                9.3121,
                93.2897
            ]
        ],
        "bids": [			
            [
                8.12,		
                0.2997		
            ],
            [
                8.1199,
                0.1998
            ]
        ]
    }
}
```
##获取各个币对的最新成交价
`Get /open/api/market`
<br>
>请求参数

无
<br>
>data说明

参考示例
<br>
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "avhbtc": "0.02000000",
        "avhusdt": "0.0100",
        "bchbtc": "0.12288899",
        "bchusdt": "760.4799",
        "btcusdt": "6189.6999",
        "eosbtc": "0.00130658",
        "eoseth": "0.02700000",
        "eosusdt": "8.0815",
        "etcbtc": "0.00249199",
        "etcusdt": "15.3999",
        "ethbtc": "0.07396799",
        "ethusdt": "457.9999",
        "icxbtc": "0.00031108",
        "icxusdt": "1.6261",
        "ltcbtc": "0.01315399",
        "ltcusdt": "81.3299",
        "xrpbtc": "0.00007843",
        "xrpusdt": "0.4853"
    }
}
```
##获取订单详情
`Get /open/api/order_info`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||symbol||string||`true`||市场标记，例：btcusdt||
||order_id||int64||`true`||订单ID||
||api_key||string||`true`||api_key||
||sign||string||`true`||签名||
>data说明

```json
"data": {
    "order_info": {
        "id": 订单id,
        "side": 买卖方向,
        "symbol": 币对标识,
        "type": 订单类型，1定价 2市价,
        "price": 价格,
        "volume": 数量,
        "status": 订单状态 0初始，1新订单，2已成交，3部分成交，4已取消，5正在取消，6已过期,
        "deal_volume": 已成交数量,
        "total_price": 当前成交总价,
        "fee": 手续费,
        "age_price": 成交均价,
        "ts": 下单时间
    },
    "trade_list": [	订单成交记录
        {
            "id": 交易id,
            "price": 成交价格,
            "volume": 成交数量,
            "direction": 主动单方向,
            "ts": 交易时间
        }
    ]
}
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "order_info": {
            "id": 900,			
            "side": "BUY",		
            "symbol": "ltcbtc",		
            "type": 1,		
            "price": 0.017006,		
            "volume": 0.01,		
            "status": 2,			
            "deal_volume": 0.01,		
            "total_price": 0.00017006,	
            "fee": 0,			
            "age_price": 0.017006,	
            "ts": 152401889365		
        },
        "trade_list": [			
            {
                "id": 442,			
                "price": 0.017006,		
                "volume": 0.01,		
                "direction": "SELL",	
                "ts": 152401889435	
            }
        ]
    }
}
```

##查询资产余额
`Get /open/api/user/account`
<br>
>请求参数

||**参数**|| **参数类型**||**必填**||**说明**||
||api_key||string||`true`||api_key||
||sign||string||`true`||签名||
>data说明

```json
"data": {
    "coin_list": [
        {
            "coin": 币种,
            "normal": 正常账户剩余资产,
            "locked": 锁定账户剩余资产
        },
    ]
}
```
>返回示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "coin_list": [
            {
                "coin": "btc",				
                "normal": 9998982.75249555,	
                "locked": 1012.2169556020048		
            },
            {
                "coin": "eth",
                "normal": 9999999.920856,
                "locked": 0.01
            },
            {
                "coin": "eos",
                "normal": 3026200.663839374,
                "locked": 5817883.48498
            },
            {
                "coin": "usdt",
                "normal": 15536399.907653771,
                "locked": 7786583.007629702
            }
        ]
    }
}
```
