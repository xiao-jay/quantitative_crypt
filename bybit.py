import logging
from datetime import datetime

import requests

import exchange_interface
import mysql
import utils
from exchange_interface import Exchange
import json
from dataclasses import dataclass
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
url = "https://api2.bybit.com/s1/byfi/get-saving-homepage-product-cards"

headers = {
    "authority": "api2.bybit.com",
    "method": "POST",
    "path": "/s1/byfi/get-saving-homepage-product-cards",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length": "133",  # 可根据实际数据调整
    "content-type": "application/json",
    "Cookie": "_by_l_g_d=ccd07054-d31d-80f4-fe95-620c3a9f0f07; deviceId=f19c38fc-d95d-d4a6-d55a-be2f8bca34c0; _fwb=239oBMQeIB96cKf9u9bUw7.1728305360944; _gcl_au=1.1.1689777108.1728305645; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22192670695dd9ea-08e3b22e7e8f6a8-16525637-1484784-192670695de1340%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22_a_u_v%22%3A%220.0.6%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyNjcwNjk1ZGQ5ZWEtMDhlM2IyMmU3ZThmNmE4LTE2NTI1NjM3LTE0ODQ3ODQtMTkyNjcwNjk1ZGUxMzQwIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; _ga=GA1.1.916788878.1729182273; _fbp=fb.1.1729182274368.986578798947179521; BYBIT_REG_REF_prod={\"lang\":\"zh-CN\",\"g\":\"ccd07054-d31d-80f4-fe95-620c3a9f0f07\",\"referrer\":\"www.google.com/\",\"source\":\"google.com\",\"medium\":\"affiliate\",\"affiliate_id\":\"3D6XLAE\",\"group_id\":\"9999\",\"group_type\":\"1\",\"url\":\"https://www.bybit.com/register?affiliate_id=3D6XLAE&group_id=9999&group_type=1&ref_code=3D6XLAE&top7&gad_source=1&gad_source=1&gclid=CjwKCAjw68K4BhAuEiwAylp3krFHqpMxDp6vR_llcs8_iUYWLtD-wWIEN0_8yq08MbR3p-CRWiFdqRoCSb0QAvD_BwE\",\"last_refresh_time\":\"Thu, 17 Oct 2024 16:24:53 GMT\"}; _gcl_aw=GCL.1729182301.CjwKCAjw68K4BhAuEiwAylp3krFHqpMxDp6vR_llcs8_iUYWLtD-wWIEN0_8yq08MbR3p-CRWiFdqRoCSb0QAvD_BwE; _gcl_gs=2.1.k1$i1729182293$u24703529; tmr_lvid=186781fcf48d7ebbb8a097821ccbf495; tmr_lvidTS=1729182303843; _ym_uid=1729182305786105710; _ym_d=1729182305; _tt_enable_cookie=1; _ttp=A97Ece_Asu3PzTowIHbDJ7B3FIg; _abck=8C2DC98122B70D122893D08F285CE723~0~YAAQjUqvi9A5Im+SAQAAp3kcoAxfcKmtu1Hlg+POdd5cMPHcUw7/70+m4kuW94M2JI6KE2R+kJ3CgMf89roR0Q6Y1JaOSxLa1tTWeu3PJ3j+G8jQBea3LlOWS9AIld1rGz/f0WgbkOjFE4lVqjg7+/ie7wBWCdUWyiydKgGqehOHMUa68i79D3LqdMQPAGzBeSkwDKXTDbV0WTMVE3Eg6It5t3bihjq2u4gZyN2OS6RHR/Nk9HH8Bw5x4ZWkvmoQvAfKLOnt8E55hklhLR89yDvRqb6j3TgTN+2In7V0e66Jj+8Ucp6QrCDW2a2/igFqM3MN/RTKfdE6b6nQHmkEX4VZyJqb0PbQm45cr44/hfwP3xxZcZg5e1DCua3fNcDR6oD0mLtI3UGijEG0dLckeCpJbipT6el3bBhdzvRxB8bkUJwpd/ZP8lABiRQRPk3qgso4HHyBeRQ=~-1~-1~-1; bm_sz=E59ADC902F11C1F8C5C90C062E4BAEB9~YAAQjUqvi9M5Im+SAQAAp3kcoBlPAsieNTwLfGlggmTtBhDkbZhdtJLk2LJue3BttFAfC48b3Wok+Y4RZaCxwoQF3mzMkdDgClyHi5mJpxn/jDyunbdVx1STr/G7tNmMI2qB3T+otI4Bvr47q/RZ+AU1Qa4F0g+lk/jRQW+myJpWZ+T89Xu4jrkRW5PpZGagt78y7WTi1iKWCez4zmXHcBnXkhA3EzKv5b5EuC2XRSt4drCABce4ZmewxutggplgfRajHiimoKLBUizT85wzOxL5Uzyod2UfC3wr1XZoiJLDEGKp3NdIFIIDwFSqdI+qv6RAcJHQChxAMI+RP0H7LYSRTjbk9+toSNFZLVkjtYEg908W8oUcayUXtJz/HvlgV2ytsVOTVcZgkYQH~3749444~3621171; BYBIT_REG_REF_EXTRA_prod={\"original_referrer\":\"www.bybit.com/zh-TW/earn/home/\",\"original_source\":\"bybit.com\",\"original_medium\":\"other\",\"original_last_url\":\"https://www.bybit.com/zh-TW/earn/savings/?homeref=1\",\"original_last_refresh_time\":\"Fri, 18 Oct 2024 14:51:15 GMT\"}; bm_mi=EAFBAA1DF573D8848A1F48E2CE42D3C9~YAAQjUqvi/o5Im+SAQAAVJccoBmM6KvyiLDuWNlGxsHoK74aJV5sZbDpnYA4UQ+kGwZnwnzdMq1g3GthB7UT6mE1NKywWLXeb7kZEDM/JCqN3aJynGchmr4edxpChUgLlYMR5KpfHsl6oxWETNstCE6/mhxUY9FufoJVzuTXYUWDMvt5/lQO1R6C2fi1sWLNav/SwEcaSP0TZh8h1bztrNrDK6nNpeXwxvXu+AcWfsIKm/bDb53koBzs9j8Hj3GlX1Xs53c5mvgpijbBfrxSd5N13TAvnbKuAATUh2A5QyzZkZVJDtpDWeuQyYQxccoLg2GlD3glsV1+l+HF1DEE~1; ak_bmsc=87C61D1180D09B27020F0F82AACB9320~000000000000000000000000000000~YAAQjUqviw86Im+SAQAAFpkcoBkzWmcurU4fBHk9T1jdE879m+9KL46koz3C9/wVccve+ADWTUpG72dW+nGjGRq62UAV/hNG4wuSgOriFZdRSrZATbVvhapW7g9epfM8rDdgoIzaFCHA5JXQqBirtPOFgXiqUclHI5C+PvC0CcVwzbQ2zRpvORu5pzAjZ6xsTi9VgqIeWMu6mVM+/3KDZMR/PzPrns9Vks1IXBl75XAtkkc4Jx3knxnxvsSTgHhW2MlVmwyooczvYHjAjNbiP0b0yB1cjoruL3lwG7TvIsVUSZaq2UFcCBqMwYo1TBvxqEbTOENH5f2K1VC+QUyhxdc2TuzQ92MvkfSk6NRHjklpWHzAVfT2PehyHDy6QmhX1jURbHK2ZH/OpCR+4r2oUsh7fh30XGFxhGJvhVzX6SLqiEsOnjIey0XAjDOok24QXyQFgw==; bm_sv=E5D449697550B3547C423FB6419B81A8~YAAQjUqvi0A6Im+SAQAAGrocoBnX0LzydS78x7I8G1O0ms6SlIBF1BGHnGxNPCCGxFGV5rdwpcRj/S3Ow3i9xbDGUXIlR+rozjoHnpxQgQnHnRPsJRMdH7l01UeyOg0ZbvGHIay31zMbzJ4gSXU+okobq3HbjiLVCc/w0pj8S+arKygF2McQWArOBg73GGgyfB9pml0JH5ilykvm+LrW9tw+keaVC3x/mfKJVKqUYewpnU/iF93QBFRICYknq1M=~1; _ga_SPS4ND2MGC=GS1.1.1729263073.2.1.1729263089.44.0.0",
    "guid": "ccd07054-d31d-80f4-fe95-620c3a9f0f07",
    "lang": "zh-TW",
    "origin": "https://www.bybit.com",
    "priority": "u=1, i",
    "referer": "https://www.bybit.com/",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "traceparent": "00-7609d07beff591f8c1123fd26471c889-52139e2428eb1a1d-00",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

# 请求体
payload = {
    "product_area": [0],
    "page": 1,
    "limit": 10,
    "product_type": 0,
    "coin_name": "",
    "sort_apr": 1,
    "match_user_asset": False,
    "show_available": False
}


class Bybit(Exchange):
    def __init__(self):
        super().__init__()
        self.exchange_name = "Bybit"

    def get_exchange_name(self) -> str:
        """获取交易所名字"""
        return self.exchange_name

    @utils.retry(max_retries=3, delay=5)
    def get_crypto_rate_data(self) -> list[mysql.CryptoRate]:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # 输出响应结果
        structured_data = convert_json_to_structure(response.json())
        cryptoRate_list = list()
        for i in structured_data.result.coin_products:
            cryptoRate = mysql.CryptoRate()
            cryptoRate.interest_rate = float(i.apy.strip('%'))
            cryptoRate.exchange_name = self.get_exchange_name()
            cryptoRate.coin_name = self.mysql.get_coin_name_by_id(i.coin)
            cryptoRate.date = datetime.now().replace(minute=0, second=0, microsecond=0)
            cryptoRate_list.append(cryptoRate)
        return cryptoRate_list

    def get_piegon_msg(self):
        # 筛选出利率大于100的币种
        filtered_rates = []
        # 构建要发送的 JSON 数据
        crypto_rate_data_list = self.get_crypto_rate_data()
        for crypto_rate_data in crypto_rate_data_list:
            if crypto_rate_data.interest_rate > 100 and crypto_rate_data.coin_name != "USDT":
                filtered_rates.append({
                    "name": crypto_rate_data.coin_name,
                    "interest_rate": crypto_rate_data.interest_rate
                })
        if len(filtered_rates) == 0:
            logging.info("no need to feishu")
            return None
        piegon_payload = exchange_interface.PigeonPayload(f"{self.get_exchange_name()}交易所"+self.get_str_rates(filtered_rates),
                                                          json.dumps(filtered_rates), "feishu")
        return piegon_payload


@dataclass
class ProductTagInfo:
    display_on_country_code: str
    display_tag_key: str
    display_mode: int


@dataclass
class SavingProduct:
    product_id: str
    coin: int
    return_coin: int
    apy: str
    product_tag_info: ProductTagInfo
    display_status: int
    tiered_apy_list: List[dict]
    tiered_non_reward_apy_e8: str
    interest_apy_e8: str
    product_type: int
    subscribe_start_at: str
    subscribe_end_at: str
    product_max_share: str
    total_deposit_share: str
    banner_info: str
    product_area: int
    staking_term: str


@dataclass
class CoinProduct:
    coin: int
    apy: str
    saving_products: List[SavingProduct]


@dataclass
class Result:
    status_code: int
    coin_products: List[CoinProduct]
    exclusive_products: List
    vip_products: List
    value_investing_products: List
    total: str


@dataclass
class Response:
    ret_code: int
    ret_msg: str
    result: Result
    ext_code: str
    ext_info: Optional[str]
    time_now: str


# Function to convert the JSON data into structured data
def convert_json_to_structure(json_data) -> Response:
    # Convert each product tag info and saving product into structured data
    coin_products = []
    for coin_product in json_data['result']['coin_products']:
        saving_products = []
        for saving_product in coin_product['saving_products']:
            tag_info = ProductTagInfo(
                display_on_country_code=saving_product['product_tag_info']['display_on_country_code'],
                display_tag_key=saving_product['product_tag_info']['display_tag_key'],
                display_mode=saving_product['product_tag_info']['display_mode']
            )
            saving_products.append(SavingProduct(
                product_id=saving_product['product_id'],
                coin=saving_product['coin'],
                return_coin=saving_product['return_coin'],
                apy=saving_product['apy'],
                product_tag_info=tag_info,
                display_status=saving_product['display_status'],
                tiered_apy_list=saving_product['tiered_apy_list'],
                tiered_non_reward_apy_e8=saving_product['tiered_non_reward_apy_e8'],
                interest_apy_e8=saving_product['interest_apy_e8'],
                product_type=saving_product['product_type'],
                subscribe_start_at=saving_product['subscribe_start_at'],
                subscribe_end_at=saving_product['subscribe_end_at'],
                product_max_share=saving_product['product_max_share'],
                total_deposit_share=saving_product['total_deposit_share'],
                banner_info=saving_product['banner_info'],
                product_area=saving_product['product_area'],
                staking_term=saving_product['staking_term']
            ))

        coin_products.append(CoinProduct(
            coin=coin_product['coin'],
            apy=coin_product['apy'],
            saving_products=saving_products
        ))

    # Create the result object
    result = Result(
        status_code=json_data['result']['status_code'],
        coin_products=coin_products,
        exclusive_products=json_data['result']['exclusive_products'],
        vip_products=json_data['result']['vip_products'],
        value_investing_products=json_data['result']['value_investing_products'],
        total=json_data['result']['total']
    )

    # Create the response object
    response = Response(
        ret_code=json_data['ret_code'],
        ret_msg=json_data['ret_msg'],
        result=result,
        ext_code=json_data['ext_code'],
        ext_info=json_data['ext_info'],
        time_now=json_data['time_now']
    )

    return response


def get_bybit_coin_data():
    url = "https://api2.bybit.com/s1/byfi/get-coins"

    try:
        # 发送 GET 请求
        response = requests.get(url)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析 JSON 响应
            data = response.json()
            return data
        else:
            logging.error(f"请求失败，状态码: {response.status_code}")
            return response.json()

    except Exception as e:
        logging.error(f"发生错误: {e}")
        return None


def insert_bybit_coin_data():
    from dataclasses import dataclass
    from typing import List, Optional

    import mysql

    @dataclass
    class Coin:
        coin: List[str]

    @dataclass
    class Result:
        status_code: int
        coins: List[Coin]

    @dataclass
    class Response:
        ret_code: int
        ret_msg: str
        result: Result
        ext_code: str
        ext_info: Optional[str]
        time_now: str

    mysql1 = mysql.Mysql_Engine()
    mysql1.create_table()
    # 解析 JSON
    response_data = get_bybit_coin_data()
    response = Response(
        ret_code=response_data['ret_code'],
        ret_msg=response_data['ret_msg'],
        result=Result(
            status_code=response_data['result']['status_code'],
            coins=[Coin(coin=coin['coin']) for coin in response_data['result']['coins']],
        ),
        ext_code=response_data['ext_code'],
        ext_info=response_data['ext_info'],
        time_now=response_data['time_now']
    )
    # 从 response 中获取 coin 数据
    if response.result.coins:
        for coin in response.result.coins:
            print(coin.coin)
            first_coin = coin.coin
            bybitCoin = mysql.BybitCoin()
            bybitCoin.coin_id = first_coin[0]
            bybitCoin.coin_name = first_coin[1]
            # 插入到数据库
            mysql.Mysql_Engine().insert_bybit_coin(bybitCoin)


if __name__ == '__main__':
    # Convert and serialize the JSON data
    bybit = Bybit()

    bybit.send_msg_to_piegon()
    # print(structured_data.result.coin_products[1].coin,structured_data.result.coin_products[1].apy)
