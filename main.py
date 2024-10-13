import mysql
import okx
import schedule
import time

def job():
    engine = mysql.get_mysql_engine()
    mysql.create_table()
    earning_list = okx.get_okx_earning_list()
    for earning in earning_list:
        mysql.insert_crypto_rate(engine, earning.invest_currency.currency_name, earning.products[0].rate.value[0])

if __name__ == '__main__':
    # 每 4 小时执行一次 job
    schedule.every(4).hours.do(job)

    while True:
        schedule.run_pending()  # 检查是否有任务需要执行
        time.sleep(1)  # 暂停 1 秒以避免 CPU 占用过高
