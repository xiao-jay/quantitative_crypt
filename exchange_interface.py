import logging
from abc import abstractmethod, ABC
import mysql
import utils


class Exchange(ABC):
    def __init__(self):
        self.enginx = mysql.get_mysql_engine()
        self.mysql = mysql.Mysql_Engine()

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
