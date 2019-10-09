

from flask import Flask
from flask_apscheduler import APScheduler
import os
    
class Config(object):
    """ 下面的各个配置项可以通过查看函数scheduler.add_job 来查看一些缺省参数以及参数的详解"""
    JOBS = [
            {
               'id':'job1',  
               'func':'timedTask:get_user_table', # timedTask:执行函数的文件，get_user_table执行函数
               'args': '',  # 执行函数需要的传递的参数，是一个元组或者list
               'trigger': {  # triggers:触发器 一次性任务triggers不用写
                    'type': 'cron',  # 定时方式，有三种，cron：定时执行的的时间，date:特定时间执行，interval：间隔时间执行
                    'day_of_week':"mon-fri", # 周一到周五
                    'hour':'0-23',  # 0点到23点
                    'minute':'0-11', # 0-11分钟
                    'second': '*/5' # 每5S  每周一到周五的每小时的0-11分钟每5S执行一次  这些时间参数都是可选的
               }
             },
             {
                "id":"job2",
                "func":"timedTask:job_1",
                "args":(3,4),
                "trigger":"interval",
                "seconds":5  # 不指定时间每5S执行一次
             }
        ]
       
    SCHEDULER_API_ENABLED = True


def get_user_table():
    filename = "./getUserInfo.py"
    os.system("python2 " + filename)


def job_1(a,b):
    print a + b


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler() # 创建定时任务
    
    # scheduler.api_enabled = True
    scheduler.init_app(app) # 初始化flask实例
    scheduler.start() # 开启定时任务，每次项目重启会执行一次定时任务再开始计时

    app.run(host="0.0.0.0", port=8081, debug=True, threaded=True)
