import configparser
import json
import logging
from abc import abstractmethod, ABC

import requests

import mysql
import utils


class PigeonPayload:
    def __init__(self, title: str, message: str, channelType: str):
        self.title = title
        self.message = message
        self.channelType = channelType

    def get_payload(self):
        return {
            "title":self.title,
            "message": self.message,
            "channelType": self.channelType
        }

class Exchange(ABC):
    def __init__(self):
        self.enginx = mysql.get_mysql_engine()
        self.mysql = mysql.Mysql_Engine()
        self.pigeon = self.get_piegon_config()

    @abstractmethod
    def get_exchange_name(self) -> str:
        """获取交易所名字"""
        raise Exception("need write get_exchange_name")

    @abstractmethod
    def get_crypto_rate_data(self) -> list[mysql.CryptoRate]:
        raise Exception("need write get_crypto_rate_data")

    @utils.retry(max_retries=3, delay=5)
    def insert_data(self) -> None:
        logging.info(f"start insert {self.get_exchange_name()} data")
        """将数据插入到数据库"""
        cryptoRate_list = self.get_crypto_rate_data()
        for cryptoRate in cryptoRate_list:
            self.mysql.insert_crypto_rate(cryptoRate)

    def get_piegon_config(self):
        config = configparser.ConfigParser()
        config.read('database.ini')
        db_config = config['pigeon']
        return db_config

    @abstractmethod
    def get_piegon_msg(self) -> PigeonPayload:
        raise Exception("need write get_piegon_msg")

    def send_msg_to_piegon(self):
        payload = self.get_piegon_msg()
        if payload is None:
            logging.info("no need send")
            return
        url = f"http://{self.pigeon['host']}:{self.pigeon['port']}/send_messages"
        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload.get_payload())

            # 检查响应状态码
            if response.status_code == 200:
                print("请求成功！")
                print("响应内容:", response.json())  # 如果响应是 JSON 格式
            else:
                print("请求失败！状态码:", response.status_code)
                print("响应内容:", response.text)

        except requests.exceptions.RequestException as e:
            print("发生异常:", e)
