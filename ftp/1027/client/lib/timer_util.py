# encoding:UTF-8
'''
参考来源
http://www.tuicool.com/articles/jInuUv
http://www.cnblogs.com/leleroyn/p/4501359.html

安装模块
pip install apscheduler

'''

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import sys
import os


# 定时任务
def tick():
    print('Tick! The time is: %s' % datetime.now())


def main():
    scheduler = BlockingScheduler()
    # second='*/5' 每5秒
    # scheduler.add_job(tick, 'cron', second='*/5', hour='*')
    # scheduler.add_job(tick, day_of_week='mon-sun', hour='12-24', minute='0-59', second='15')
    scheduler.add_job(tick, 'cron', day_of_week='0-7', hour='*', minute='*', second='*/5')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    scheduler.start()


if __name__ == "__main__":
    sys.exit(main())
