# -*- coding: utf-8 -*-
# @time     : 2019/1/9 0009 下午 23:02
# @Author   : yuxuan
# #file     : webservice_request.py


# 封装webservice协议请求方法

from suds.client import Client


class WebserviceRequest:

    def __init__(self, url):

        try:
            self.client = Client(url=url)
        except Exception as e:
            raise e

    def get_result(self, port_name , data):     # port_name 为接口名称
        try:
            req = 'self.client.service.' + port_name + '(data)'
            resp = eval(req)
            return resp
        except Exception as e:
            raise e





if __name__ == '__main__':

    url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    port_name = 'sendMCode'
    data = {"client_ip":"192.168.5.80","tmpl_id":1,"mobile":15156602357}
    result = WebserviceRequest(url).get_result(port_name,data)
    print('请求结果是{0}'.format(result))







