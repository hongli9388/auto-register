# -*- coding: utf-8 -*-
# @time     : 2019/1/11 0011 下午 18:28
# @Author   : yuxuan
# #file     : logger.py


# 封装日志类，根据日期目录按日志级别存放
# 步骤：
# 1.定义日志收集器和收集级别
# 2.设定输出渠道
# 3.对接

import logging
from logging.handlers import RotatingFileHandler

import time
from common import project_path
import os
from common.read_conf import ReadConfig
import HTMLTestRunnerNew


logger = logging.getLogger(ReadConfig().get('LOG','log_name'))
logger.setLevel(ReadConfig().get('LOG', 'collect_leave'))

# 获取创建日志的目录
def get_dir():
    log_dir = os.path.join(project_path.log_dir, get_current())
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    else:
        return log_dir


# 获取系统当前时间的年月日格式
def get_current():
    return time.strftime('%Y%m%d', time.localtime())


# 添加渠道
def add_handler(level):
    if level == 'error':
        logger.addHandler(MyLog.error_handler)   # 如果级别是error，日志就放到error渠道
    else:
        logger.addHandler(MyLog.info_handler)   # 其他放到info渠道
    logger.addHandler(MyLog.ch)                 # 全部输出到控制台
    logger.addHandler(MyLog.report_handler)     # 全部输出到报表


# 去重
def remove_handler(level):
    if level == 'error':
        logger.removeHandler(MyLog.error_handler)
    else:
        logger.removeHandler(MyLog.info_handler)
    logger.removeHandler(MyLog.ch)
    logger.removeHandler(MyLog.report_handler)



class MyLog:


    log_dir = os.path.join(project_path.log_dir, get_dir())
    info_path = os.path.join(log_dir,'info.log')
    error_path = os.path.join(log_dir, 'error.log')

    # 定义输出格式
    formatter = logging.Formatter(ReadConfig().get('LOG', 'formatter'))
    # 定义控制台渠道
    ch = logging.StreamHandler()
    ch.setLevel(ReadConfig().get('LOG', 'console_leave'))
    ch.setFormatter(formatter)

    # 定义info级别文件输出渠道
    info_handler = logging.handlers.RotatingFileHandler(info_path, maxBytes=10*1024*1024, backupCount=3, encoding='utf-8')
    info_handler.setLevel('INFO')
    info_handler.setFormatter(formatter)

    # 定义error级别文件输出渠道
    error_handler = logging.handlers.RotatingFileHandler(error_path, maxBytes=10*1024*1024, backupCount=3, encoding='utf-8')
    error_handler.setLevel('ERROR')
    error_handler.setFormatter(formatter)

    # 定义报表渠道
    report_handler = logging.StreamHandler(HTMLTestRunnerNew.stdout_redirector)
    report_handler.setLevel(ReadConfig().get('LOG', 'report_leave'))
    report_handler.setFormatter(formatter)


    @staticmethod
    def debug(msg):
        add_handler('debug')
        logger.debug(msg)
        remove_handler('debug')

    @staticmethod
    def info(msg):
        add_handler('info')
        logger.info(msg)
        remove_handler('info')

    @staticmethod
    def error(msg):
        add_handler('error')
        logger.error(msg, exc_info=True)
        remove_handler('error')




if __name__ == '__main__':
    my_logger = MyLog()
    my_logger.debug('dfaf')
    my_logger.info('gbdfh')
    my_logger.error('today')











