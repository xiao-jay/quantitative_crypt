import logging

import requests

url = "https://www.okx.com/priapi/v1/earn/simple-earn/all-products?type=all&t=1728808412672"

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "App-Type": "web",
    "Cookie": "ok_prefer_udColor=0; browserVersionLevel=v5.6ad2a8e37c01; devId=b96c2994-b583-478a-9df7-7975d7dd73a0; _ym_uid=1713063029206046708; _ym_d=1713063029; ok_prefer_udTimeZone=2; preferLocale=zh_CN; intercom-device-id-ny9cf50h=fc4b90bb-7021-45f6-90b1-794cef7bec55; locale=zh_CN; amp_669cbf=b96c2994-b583-478a-9df7-7975d7dd73a0.Yjk2YzI5OTQtYjU4My00NzhhLTlkZjctNzk3NWQ3ZGQ3M2Ew..1i12jtnav.1i12jtnb3.c.6.i; ok_site_info===QfxojI5RXa05WZiwiIMFkQPx0Rfh1SPJiOiUGZvNmIsIyVUJiOi42bpdWZyJye; first_ref=https%3A%2F%2Fwww.google.com%2F; intercom-id-ny9cf50h=e05f9701-6cb3-40fc-84dd-c7033d368733; intercom-session-ny9cf50h=; fingerprint_id=b96c2994-b583-478a-9df7-7975d7dd73a0; ok_prefer_currency=%7B%22currencyId%22%3A0%2C%22isDefault%22%3A1%2C%22isPremium%22%3Afalse%2C%22isoCode%22%3A%22USD%22%2C%22precision%22%3A2%2C%22symbol%22%3A%22%24%22%2C%22usdToThisRate%22%3A1%2C%22usdToThisRatePremium%22%3A1%2C%22displayName%22%3A%22%E7%BE%8E%E5%85%83%22%7D; ok-exp-time=1728798010716; _gid=GA1.2.1817616402.1728798013; _ym_isad=2; __cf_bm=YqFM9wFky5SoVg6lbBR2UZq6S.dFTPm8f8kySEQgwSw-1728807791-1.0.1.1-vh5JmLdJEcPR5yykkxgENt6bDEiYnsT1Iilm9I8faS4AGVEzn0zfj.X2ghKwutQpgFu8KnjI_nvWX996_UQSXA; okg.currentMedia=md; traceId=2140688084095770001; amp_56bf9d=b96c2994-b583-478a-9df7-7975d7dd73a0.SXRXUG5QaXFvb1RvV004cEJkMytyUT09..1ia2g5nol.1ia2g5noo.aa.14.be; _monitor_extras={\"deviceId\":\"ADHoSwgA286EC4Xgz85t7O\",\"eventId\":371,\"sequenceNumber\":371}; ok-ses-id=cMfH1AwYwwxUr0IJ2tWIwD28d/MbVRsY5krlxGuLNtmQ9ZVLfh/bd3vQ9aJ43UPijLNGBT4jyhI5aaz3yoKfYc+c0UPPyNnaWNbLktLthOUet9jiL8WV35/5FZZqzw5k; _gat_UA-35324627-3=1; _ga=GA1.1.478797413.1713063021; _ga_G0EKWWQGTZ=GS1.1.1728808409.13.1.1728808412.57.0.0",
    "DevId": "b96c2994-b583-478a-9df7-7975d7dd73a0",
    "Referer": "https://www.okx.com/zh-hans/earn/simple-earn",
    "Sec-CH-UA": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "X-Cdn": "https://www.okx.com",
    "X-Id-Group": "2140688084095770001-c-9",
    "X-Locale": "zh_CN",
    "X-Site-Info": "==QfxojI5RXa05WZiwiIMFkQPx0Rfh1SPJiOiUGZvNmIsIyVUJiOi42bpdWZyJye",
    "X-Utc": "8"
}

import requests


class Currency:
    def __init__(self, currency_icon, currency_id, currency_name):
        self.currency_icon = currency_icon
        self.currency_id = currency_id
        self.currency_name = currency_name


class Rate:
    def __init__(self, value, rate_type):
        self.value = value
        self.rate_type = rate_type


class Term:
    def __init__(self, labels, show, term_type, value):
        self.labels = labels
        self.show = show
        self.term_type = term_type
        self.value = value


class Product:
    def __init__(self, activity_period_end_date, bonus_currency, campaign_uid,
                 interest_currency, is_learn_and_earn, labels, lock_up_period,
                 products_type, purchase_status, rate, saving_type, term, product_type):
        self.activity_period_end_date = activity_period_end_date
        self.bonus_currency = bonus_currency
        self.campaign_uid = campaign_uid
        self.interest_currency = interest_currency
        self.is_learn_and_earn = is_learn_and_earn
        self.labels = labels
        self.lock_up_period = lock_up_period
        self.products_type = products_type
        self.purchase_status = purchase_status
        self.rate = rate
        self.saving_type = saving_type
        self.term = term
        self.type = product_type


class EarningsData:
    def __init__(self, balance, invest_currency, labels, product_eng_name,
                 products, products_type, rate, redirect_url, saving_type,
                 term, data_type, valuation_usd):
        self.balance = balance
        self.invest_currency = invest_currency
        self.labels = labels
        self.product_eng_name = product_eng_name
        self.products = products
        self.products_type = products_type
        self.rate = rate
        self.redirect_url = redirect_url
        self.saving_type = saving_type
        self.term = term
        self.type = data_type
        self.valuation_usd = valuation_usd


def parse_currency(data):
    return Currency(
        currency_icon=data['currencyIcon'],
        currency_id=data['currencyId'],
        currency_name=data['currencyName']
    )


def parse_rate(data):
    return Rate(
        value=data['rateNum']['value'],
        rate_type=data['rateType']
    )


def parse_term(data):
    return Term(
        labels=data['labels'],
        show=data['show'],
        term_type=data['type'],
        value=data['value']
    )


def parse_product(data):
    return Product(
        activity_period_end_date=data.get('activityPeriodEndDate'),
        bonus_currency=data.get('bonusCurrency'),
        campaign_uid=data.get('campaignUid', ''),
        interest_currency=parse_currency(data['interestCurrency']),
        is_learn_and_earn=data['isLearnAndEarn'],
        labels=data['labels'],
        lock_up_period=data['lockUpPeriod'],
        products_type=data['productsType'],
        purchase_status=data['purchaseStatus'],
        rate=parse_rate(data['rate']),
        saving_type=data['savingType'],
        term=parse_term(data['term']),
        product_type=data['type']
    )


def parse_earnings_data(data):
    return EarningsData(
        balance=data['balance'],
        invest_currency=parse_currency(data['investCurrency']),
        labels=data['labels'],
        product_eng_name=data['productEngName'],
        products=[parse_product(product) for product in data['products']],
        products_type=data['productsType'],
        rate=parse_rate(data['rate']),
        redirect_url=data['redirectUrl'],
        saving_type=data['savingType'],
        term=parse_term(data['term']),
        data_type=data['type'],
        valuation_usd=data['valuationUSD']
    )


def get_top_earnings(earnings_list, top_n=10):
    # 按照每个 earnings_data 的 valuation_usd 排序
    sorted_earnings = sorted(earnings_list, key=lambda e: float(e.products[0].rate.value[0]), reverse=True)
    # 返回前 top_n 个
    return sorted_earnings[:top_n]


def get_okx_earning_list() -> [EarningsData]:
    response = requests.get(url, headers=headers)
    earnings_datas = []
    # 解析 JSON 数据
    if response.status_code == 200:
        json_data = response.json()
        for currencie in json_data["data"]["allProducts"]["currencies"]:
            earnings_data = parse_earnings_data(currencie)
            earnings_datas.append(earnings_data)
    else:
        logging.info(f"请求失败，状态码: {response.status_code}")
    return earnings_datas


def get_okx_top_earnings(top_n=10)-> [EarningsData]:
    earnings_datas = get_okx_earning_list()
    top_earnings = get_top_earnings(earnings_datas, top_n)
    for earnings in top_earnings:
        logging.info(f"投资货币: {earnings.invest_currency.currency_name}, 利率: {earnings.products[0].rate.value[0]}")
    return top_earnings
