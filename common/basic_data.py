# -*- coding: utf-8 -*-
# @time     : 2019/1/10 0010 下午 16:33
# @Author   : yuxuan
# #file     : basic_data.py


# 正则查找并替换
import re



class DoRegex:

    @staticmethod       # 不需要传递参数，采用静态方法
    def replace(target):    # target为目标字符串
        pattern = '\$\{(.*?)\}'
        while re.search(pattern, target):    # 循环如果查到目标字符串
            key = re.search(pattern, target).group(1)
            from common.basic_data import Context
            new = getattr(Context, key)
            target = re.sub(pattern, new, target, count=1)    # 每循环一次，执行查找并替换一个
        return target



# if __name__ == '__main__':
#     import json
#     data = '{"uid":${uid}, "true_name": "${true_name}", "cre_id": "${cre_id}"}'
#     data = DoRegex().replace(data)
#     data = json.loads(data)
#     print(data)









from common.read_conf import ReadConfig
from common import mobile_phone
from common import random_string



class Context:

    rf = ReadConfig()
    client_ip = rf.get('basic', 'client_ip')
    tmpl_id = rf.get('basic', 'tmpl_id')
    true_name = rf.get('basic', 'true_name')
    normal_mobile = mobile_phone.creat_mobile()
    user_id = random_string.create_str()






