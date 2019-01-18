# -*- coding: utf-8 -*-
# @time     : 2019/1/13 0013 下午 21:13
# @Author   : yuxuan
# #file     : test_userAuth.py

import unittest
from common.do_excel import DoExcel
from ddt import ddt, data
from common.basic_data import DoRegex, Context
from common import project_path
from common.read_conf import ReadConfig
import json
from common.webservice_request import WebserviceRequest
from common.do_mysql import DoMysql
from common.create_id_card import get_card_id
import time
from common.logger import MyLog




do_excel = DoExcel(project_path.data_path)
cases = do_excel.get_cases('verifiedUserAuth')
my_logger = MyLog()


@ddt
class TestUserAuth(unittest.TestCase):


    def setUp(self):
        self.db = DoMysql()
        # 随机产生身份证号，放入上下文
        ID_card_No = get_card_id()
        setattr(Context, 'cre_id', ID_card_No)
        #实名认证前查询实名认证表记录
        auth_sql = 'SELECT COUNT(*) count FROM user_db.t_user_auth_info;'
        self.before_auth_count = self.db.fetch_one(auth_sql)['count']


    @data(*cases)
    def test_user_auth(self, case):
        my_logger.info('正在执行第{}条用例:{}'.format(case.case_id, case.title))
        my_logger.info('-----------开始检查url地址-------------')
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        my_logger.info('请求url:{}'.format(url))
        data = DoRegex().replace(case.data)
        data = json.loads(data)
        my_logger.info('-----------开始检查参数-------------')
        my_logger.info('请求参数:{}'.format(data))
        res = WebserviceRequest(url).get_result(case.port_name, data)
        time.sleep(60)
        my_logger.info('请求结果:{}'.format(res))
        try:
            self.assertEqual(case.expected, res['retInfo'])
            do_excel.bace_write_by_case_id('verifiedUserAuth', case.case_id, str(res), 'success')
            Test_result = 'pass'
        except AssertionError as e:
            my_logger.error('出错了,{}'.format(e))
            do_excel.bace_write_by_case_id('verifiedUserAuth', case.case_id, str(res), 'fail')
            Test_result = 'fail'
            raise e
        except Exception as e:
            raise e

        my_logger.info('本条用例测试结果:{}'.format(Test_result))



        # 如果发送短信验证码成功
        if res['retCode'] == '0' and case.port_name == 'sendMCode':
            sql_code = 'SELECT Fverify_code FROM sms_db_20.t_mvcode_info_3 where Fmobile_no={0};'.format(getattr(Context, 'normal_mobile'))
            verify_code = DoMysql().fetch_one(sql_code)['Fverify_code']
            if verify_code:  # 如果查到验证码就放入上下文
                setattr(Context, 'verify_code', verify_code)


        # 如果注册成功，查询uid放入上下文
        if res['retCode'] == '0' and case.port_name == 'userRegister':
            sql_uid = "SELECT Fuid uid FROM user_db.t_user_info where Fuser_id='{0}' and Fip='{1}' ORDER BY Fcreate_time DESC;".format(getattr(Context, 'user_id'), Context.client_ip)
            uid = str(DoMysql().fetch_one(sql_uid)['uid'])
            if uid:    # 如果查询到Fuid就放入上下文
                setattr(Context, 'uid', uid)

        # 实名认证成功后，数据验证,验证数据库影响行数是否为1
        if res['retCode'] == '0' and case.port_name == 'verifyUserAuth':
            expected = self.before_auth_count + 1                                 # 预期结果=实名认证前记录数 + 1
            auth_sql = 'SELECT COUNT(*) count FROM user_db.t_user_auth_info;'   # 实名认证成功后再次查询记录数
            actual = DoMysql().fetch_one(auth_sql)['count']
            self.assertEqual(expected, actual)
            my_logger.info('实名认证成功后,查询影响实名认证表行数等于1')


    def tearDown(self):
        self.db.close()
        my_logger.info('关闭数据库连接，测试环境还原')





