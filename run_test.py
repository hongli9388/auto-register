# -*- coding: utf-8 -*-
# @time     : 2019/1/18 0018 上午 11:49
# @Author   : yuxuan
# #file     : run_test.py

# 运行所有的测试类

import unittest
from common import project_path
import HTMLTestRunnerNew


discover = unittest.defaultTestLoader.discover(project_path.test_dir, pattern='test*.py', top_level_dir=None)
with open(project_path.report_path, 'wb+') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, title='用户注册接口', description='完成用户注册操作', tester='yuxuan')
    runner.run(discover)



