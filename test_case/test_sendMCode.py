# -*- coding: utf-8 -*-
# @time     : 2019/1/10 0010 下午 18:34
# @Author   : yuxuan
# #file     : test_sendMCode.py

# 编写发送短信验证码测试类


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
from common.logger import MyLog



do_excel = DoExcel(project_path.data_path)
cases = do_excel.get_cases('sendMcode')
my_logger = MyLog()


@ddt
class TestSendMCode(unittest.TestCase):

    def setUp(self):

        self.do_mysql = DoMysql()
        mobile = mobile_phone.creat_mobile()
        setattr(Context, 'mobile', mobile)

    @data(*cases)
    def test_send_Mcode(self, case):
        my_logger.info('正在执行第{}条用例:{}'.format(case.case_id, case.title))
        my_logger.info('-----------开始检查url地址-------------')
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        my_logger.info('请求url:{}'.format(url))
        data = DoRegex().replace(case.data)
        data = json.loads(data)
        my_logger.info('-----------开始检查请求参数-------------')
        my_logger.info('请求参数:{}'.format(data))
        try:
            resp = WebserviceRequest(url).get_result(case.port_name, data)
            time.sleep(60)
            my_logger.info('请求接口结果:{}'.format(resp))
            if resp['retCode'] == '0':
                self.assertEqual(case.expected, resp['retInfo'])
                do_excel.bace_write_by_case_id('sendMcode', case.case_id, str(resp), 'success')
                Test_result = 'pass'

                # 数据验证
                sql = 'SELECT * FROM sms_db_20.t_mvcode_info_3 where Fmobile_no={};'.format(getattr(Context, 'mobile'))
                seek_data = self.do_mysql.fetch_one(sql)
                actual = {"client_ip": seek_data['Fclient_ip'], "tmpl_id": str(seek_data['Ftmpl_id']),
                          "mobile": str(seek_data['Fmobile_no'])}
                self.assertDictEqual(data, actual)
                my_logger.info('发送验证码成功，查询数据库，添加一条数据与请求参数相同')
        except Exception as e:
            # 异常测试用例，需要捕捉错误信息进行断言
            self.assertIn(case.expected, str(e))
            do_excel.bace_write_by_case_id('sendMcode', case.case_id, str(e.__dict__['fault'][1]), 'success')
            sql = 'SELECT * FROM sms_db_20.t_mvcode_info_3 where Fmobile_no={};'.format(getattr(Context, 'mobile'))
            seek_data = self.do_mysql.fetch_one(sql)
            expected = None
            self.assertEqual(expected, seek_data)
            my_logger.info('发送验证码成功，数据库查询无数据')
            Test_result = 'pass'
        except AssertionError as e:
            Test_result = 'fail'
            my_logger.error('出错了,{}'.format(e))
            do_excel.bace_write_by_case_id('sendMcode', case.case_id, e, 'fail')
            raise e

        my_logger.info('本条用例测试结果:{}'.format(Test_result))


    def tearDown(self):
        self.do_mysql.close()
        my_logger.info('关闭数据库连接，测试环境还原')


