# -*- coding: utf-8 -*-
# @time     : 2019/1/10 0010 下午 15:52
# @Author   : yuxuan
# #file     : mobile_phone.py

import random
#随机产生手机号，尾号后三位固定不变
def creat_mobile():
    second = [3,5,7,8][random.randint(0,3)]
    third = {3:random.randint(0,9), 5:[i for i in range(10) if i !=4][random.randint(0,8)],
             7:[6,7][random.randint(0,1)], 8:random.randint(0,9)}[second]
    # 中间5位随机
    middle = random.randint(9999,100000)
    # 尾号最后3位固定不变
    last_three = 320
    #拼接后的手机号
    return '1{}{}{}{}'.format(second, third, middle, last_three)



if __name__ == '__main__':
    mobile = creat_mobile()
    print(mobile)



