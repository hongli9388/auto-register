# -*- coding: utf-8 -*-
# @time     : 2019/1/12 0012 下午 15:59
# @Author   : yuxuan
# #file     : test_register.py

import unittest
from common import mobile_phone
from common.do_excel import DoExcel
from ddt import ddt, data
from common.basic_data import DoRegex, Context
from common import project_path
from common.read_conf import ReadConfig
import json
import time
from common.webservice_request import WebserviceRequest
from common.do_mysql import DoMysql
import random
from common import random_string
from common.logger import MyLog





# 读取测试数据
do_excel = DoExcel(project_path.data_path)
cases = do_excel.get_cases('register')
my_logger = MyLog()


@ddt
class TestRegister(unittest.TestCase):



    def setUp(self):
        self.db = DoMysql()
        sql = 'SELECT COUNT(*) count FROM user_db.t_user_info;'
        self.before_line_count = self.db.fetch_one(sql)['count']



    @data(*cases)
    def test_register(self, case):
        my_logger.info('正在执行第{}条用例:{}'.format(case.case_id, case.title))
        my_logger.info('-----------开始检查url地址-------------')
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        my_logger.info('请求url:{}'.format(url))
        # 因注册的用户名不能重复，做随机处理
        last_user_id = random_string.create_str()
        setattr(Context, 'user_id', last_user_id)
        # 因测试验证码超时需要新的手机号验证
        if case.title == '发送短信验证码用于超时':
            normal_mobile = mobile_phone.creat_mobile()
            setattr(Context, 'normal_mobile', normal_mobile)
        data = DoRegex.replace(case.data)
        data = json.loads(data)
        my_logger.info('-----------开始检查参数-------------')
        my_logger.info('注册请求参数:{0}'.format(data))
        if case.title == '注册验证码超时':
            time.sleep(500)
        else:
            time.sleep(60)
        res = WebserviceRequest(url).get_result(case.port_name, data)
        my_logger.info('注册接口请求结果:{}'.format(res))
        try:
            self.assertEqual(case.expected, res['retInfo'])
            do_excel.bace_write_by_case_id('register', case.case_id, str(res), 'success')
            Test_result = 'pass'

        except AssertionError as e:
            my_logger.error('出错了,{}'.format(e))
            do_excel.bace_write_by_case_id('register', case.case_id, str(res), 'fail')
            Test_result = 'fail'
            raise e
        except Exception as e:
            raise e

        my_logger.info('本条用例测试结果:{}'.format(Test_result))


        if case.title == '成功发送短信验证码':  # 如果发送短信验证码成功请求成功，查询验证码
            sql_code = 'SELECT Fverify_code FROM sms_db_20.t_mvcode_info_3 where Fmobile_no={0};'.format(getattr(Context, 'normal_mobile'))
            verify_code = DoMysql().fetch_one(sql_code)['Fverify_code']
            if verify_code:  # 如果查到验证码就放入上下文
                setattr(Context, 'verify_code', verify_code)
            else:  # 如果为空，上下文中验证码为空
                setattr(Context, 'verify_code', None)

        # 注册成功数据验证
        if res['retCode'] == '0' and case.port_name == 'userRegister':

            # 验证如果注册成功，影响数据库的行数是否等于1
            expected = self.before_line_count + 1  # 期望结果=请求前行数 + 1
            # print('期望结果:', expected)
            sql2 = 'SELECT COUNT(*) count FROM user_db.t_user_info;'
            actual = DoMysql().fetch_one(sql2)['count']  # 实际结果=请求注册后行数
            # print('实际结果:', actual)
            self.assertEqual(expected, actual)
            my_logger.info('请求注册接口成功后，查询影响t_user_info表行数等于1')


    def tearDown(self):
        self.db.close()
        my_logger.info('关闭数据库连接，测试环境还原')


