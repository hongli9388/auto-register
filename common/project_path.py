# -*- coding: utf-8 -*-
# @time     : 2019/1/10 0010 下午 16:39
# @Author   : yuxuan
# #file     : project_path.py

# 定义项目文件常量路径

import os

# 项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)

# 配置文件目录
conf_dir = os.path.join(base_dir, 'conf')
# print(conf_dir)

# 测试数据目录
data_dir = os.path.join(base_dir, 'test_data')
data_path = os.path.join(data_dir, 'auto_test_register.xlsx')
# print(data_path)

# 日志目录
log_dir = os.path.join(base_dir, 'log')
# print(log_dir)

# 测试报告目录
report_dir = os.path.join(base_dir, 'reports')
report_path = os.path.join(base_dir, r'reports\auto_test_registers.html')
print(report_path)

# 编写接口测试类目录
test_dir = os.path.join(base_dir, 'test_case')
# print(test_dir)

