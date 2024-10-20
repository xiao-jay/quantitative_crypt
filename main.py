import logging
import bybit
import mysql
import okx
import schedule
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def job():
    okx1 = okx.OKX()
    okx1.insert_data()


def job2():
    bit = bybit.Bybit()
    bit.insert_data()

def job3():
    bit = bybit.Bybit()
    bit.send_msg_to_piegon()
    okx1 = okx.OKX()
    okx1.send_msg_to_piegon()

if __name__ == '__main__':
    # 每 4 小时执行一次 job
    logging.info("start main")
    schedule.every(4).hours.do(job)
    schedule.every(4).hours.do(job2)
    schedule.every(1).hours.do(job3)
    mysql = mysql.Mysql_Engine()
    mysql.create_table()

    while True:
        schedule.run_pending()  # 检查是否有任务需要执行
        time.sleep(1)  # 暂停 1 秒以避免 CPU 占用过高

