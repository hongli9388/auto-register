# -*- coding: utf-8 -*-
# @time     : 2019/1/10 0010 下午 16:37
# @Author   : yuxuan
# #file     : read_conf.py

# 封装读取配置文件类

import configparser
from common import project_path
import os


class ReadConfig:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        file_name = os.path.join(project_path.conf_dir,'switch.conf')
        self.cf.read(filenames=file_name,encoding='utf-8')
        if self.cf.getboolean(section='button', option='on'):    # 判断如果为true就读取第一套环境信息，否则读取第二套环境信息
            file_name1 = os.path.join(project_path.conf_dir, 'test_env_1.conf')
            self.cf.read(filenames=file_name1, encoding='utf-8')
        else:
            file_name2 = os.path.join(project_path.conf_dir, 'test_env_2.conf')
            self.cf.read(filenames=file_name2, encoding='utf-8')


    def get(self, section, option):
        return self.cf.get(section, option)


    def get_bool(self, section, option):
        return self.cf.getboolean(section, option)

    def get_int(self, section, option):
        return self.cf.getint(section, option)



if __name__ == '__main__':
    ip = ReadConfig().get('basic', 'client_ip')
    print(ip)

