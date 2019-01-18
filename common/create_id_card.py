# -*- coding: utf-8 -*-
# @time     : 2019/1/13 0013 下午 22:40
# @Author   : yuxuan
# #file     : create_id_card.py

import random
import time


def getValidateCheckout(id17):
    # 获得校验码算法
    weight=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]            # 十七位数字本体码权重
    validate=['1','0','X','9','8','7','6','5','4','3','2']  # mod11,对应校验码字符值

    sum=0
    mode=0
    for i in range(0,len(id17)):
        sum = sum + int(id17[i])*weight[i]
    mode=sum%11
    return validate[mode]



def get_areaid():
    area_list = ['110227', '411523', '410101', '411501', '310101', '320611', '420106', '500233', '350501', '370211', '340104']
    area_id = random.choice(area_list)     # 前6位地区号
    return str(area_id)

def get_year():
    year = random.randint(1949, int(time.strftime('%Y', time.localtime())) - 18)
    return str(year)

def get_month():

    month = random.randint(1, 12)
    if month <10:
        month = '0' + str(month)
        return month
    else:
        return month

def get_day():
    day = random.randint(1,31)
    if day < 10:
        day = '0' + str(day)
        return day
    else:
        return day

def get_sequence_code():

    code = random.randint(1,999)
    if code <10:
        code = '00' + str(code)
        return code
    elif code <100:
        code = '0' + str(code)
        return code
    elif code <999:
        code = str(code)
        return code

def get_card_id():
    area_id = str(get_areaid())   # 地区前6位
    year = str(get_year())          # 年份
    month = str(get_month())        # 月份
    day = str(get_day())            #日
    sequence_code = str(get_sequence_code())  # 3位顺序码
    card_id = area_id+year+month+day+sequence_code   # 校验码

    last_code = str(getValidateCheckout(card_id))
    last_card_id = card_id + last_code
    return last_card_id



if __name__ == '__main__':
    print(get_card_id())








