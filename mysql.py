import configparser
import logging

import mysql

from sqlalchemy import create_engine, Column, String, Float, Integer, DATETIME, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_mysql_engine():
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('database.ini')

    db_config = config['mysql']
    # 创建数据库引擎和会话工厂
    engine = create_engine(
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    return engine


# 定义基类
Base = declarative_base()


# 定义数据模型
class CryptoRate(Base):
    __tablename__ = 'crypto_rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DATETIME, nullable=False)
    coin_name = Column(String(50), nullable=False)
    interest_rate = Column(Float, nullable=False)
    exchange_name = Column(String(255), nullable=True)


# 定义 BybitCoin 类
class BybitCoin(Base):
    __tablename__ = 'bybit_coin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_name = Column(String(100), nullable=False)
    coin_id = Column(String(100), nullable=False)


class Mysql_Engine():
    def __init__(self):
        self.engine = mysql.get_mysql_engine()

    def create_table(self):
        # 创建表
        inspector = inspect(self.engine)
        if 'crypto_rates' not in inspector.get_table_names():
            Base.metadata.create_all(self.engine, tables=[CryptoRate.__table__])
            logging.info("Table created successfully.")

        if 'bybit_coin' not in inspector.get_table_names():
            Base.metadata.create_all(self.engine, tables=[BybitCoin.__table__])
            logging.info("Table created successfully.")

    def insert_crypto_rate(self, cryptoRate: CryptoRate) -> None:
        # 创建会话
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            # 当前时间
            # 查询数据是否存在
            existing_rate = session.query(CryptoRate).filter(
                CryptoRate.date == cryptoRate.date,
                CryptoRate.coin_name == cryptoRate.coin_name
            ).first()

            # 如果不存在，则插入新记录
            if existing_rate is None:
                session.add(cryptoRate)
                session.commit()
                logging.info(f'Inserted: {cryptoRate.coin_name}')
            else:
                logging.info('Data already exists, no insertion performed.')
        except Exception as e:
            logging.info(f'An error occurred: {e}')
            session.rollback()  # 回滚事务
        finally:
            session.close()  # 确保关闭会话

    # 根据 coin_id 查询 coin_name
    def get_coin_name_by_id(self, coin_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        coin = session.query(BybitCoin).filter(BybitCoin.coin_id == coin_id).first()
        session.close()
        return coin.coin_name if coin else None

    def insert_bybit_coin(self, bybitCoin: BybitCoin) -> None:
        # 创建会话
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            # 当前时间
            # 查询数据是否存在
            existing_rate = session.query(BybitCoin).filter(
                BybitCoin.coin_id == bybitCoin.coin_id,
                BybitCoin.coin_name == bybitCoin.coin_name
            ).first()
            # 如果不存在，则插入新记录
            if existing_rate is None:
                session.add(bybitCoin)
                session.commit()
                logging.info(f'Inserted: {bybitCoin.coin_name}')
            else:
                logging.info('Data already exists, no insertion performed.')
        except Exception as e:
            logging.info(f'An error occurred: {e}')
            session.rollback()  # 回滚事务
        finally:
            session.close()  # 确保关闭会话
