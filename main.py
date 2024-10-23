import logging
import bybit
import okx
import schedule
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job():
    okx1 = okx.OKX()
    okx1.insert_data()
    okx1.mysql.engine.dispose()

    bit = bybit.Bybit()
    bit.insert_data()
    bit.mysql.engine.dispose()

def job2():
    bit = bybit.Bybit()
    bit.send_msg_to_piegon()
    bit.mysql.engine.dispose()

    okx1 = okx.OKX()
    okx1.send_msg_to_piegon()
    okx1.mysql.engine.dispose()


class Job_Data:
    def __init__(self, job_func, time_interval):
        self.job_func = job_func
        self.interval = time_interval


job_list = [Job_Data(job, 4*60), Job_Data(job2, 60)]

if __name__ == '__main__':
    # mysql = mysql.Mysql_Engine()
    # mysql.create_table()

    # 每 4 小时执行一次 job
    logging.info("start main")
    for job in job_list:
        job.job_func()
        schedule.every(job.interval).minutes.do(job.job_func)

    while True:
        schedule.run_pending()  # 检查是否有任务需要执行
        time.sleep(1)  # 暂停 1 秒以避免 CPU 占用过高
