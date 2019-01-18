# -*- coding: utf-8 -*-
# @time     : 2019/1/12 0012 下午 20:07
# @Author   : yuxuan
# #file     : random_string.py

# 创建4位随机字母 用于注册用户名
import random

def create_str():
    s = ''
    for i in range(4):
        s1 = chr(random.randint(97, 122))
        s += str(s1)
    last_user_id = s + '{0}{1}'.format('雨轩', random.randint(0, 100))
    return last_user_id




if __name__ == '__main__':
    s = create_str()
    print(s)









