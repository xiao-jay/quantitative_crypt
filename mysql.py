
import configparser
import logging
from datetime import datetime

from sqlalchemy import create_engine, Column, String, Float, Date, Integer, DATETIME, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker


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

def create_table():
    engine = get_mysql_engine()
    # 创建表
    inspector = inspect(engine)
    if 'crypto_rates' not in inspector.get_table_names():
        Base.metadata.create_all(engine)
        logging.info("Table created successfully.")



def insert_crypto_rate(engine, coin_name, interest_rate):
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 当前时间
        current_time = datetime.now().replace(minute=0, second=0, microsecond=0)

        # 查询数据是否存在
        existing_rate = session.query(CryptoRate).filter(
            CryptoRate.date == current_time,
            CryptoRate.coin_name == coin_name
        ).first()

        # 如果不存在，则插入新记录
        if existing_rate is None:
            new_rate = CryptoRate(date=current_time, coin_name=coin_name, interest_rate=interest_rate)
            session.add(new_rate)
            session.commit()
            logging.info(f'Inserted: {new_rate.coin_name}')
        else:
            logging.info('Data already exists, no insertion performed.')
    except Exception as e:
        logging.info(f'An error occurred: {e}')
        session.rollback()  # 回滚事务
    finally:
        session.close()  # 确保关闭会话