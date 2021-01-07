
import requests
import logging
from django.utils.deprecation import MiddlewareMixin
import uuid
import datetime
import hashlib
logger = logging.getLogger()


class ExceptionLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        import traceback
        logger.error(traceback.format_exc())


def get_student_status(id_card):

    url='http://jiankangapi.capcloud.com.cn:8088/api/query/healthyQueryV3'

    appid='44ea00af-b373-4764-9a7b-5b22bf71e3d3'
    secret = '8ae9f797cde22a14b4d8ebb5654a4eda'
    nonce_str = str(uuid.uuid4()).replace('-','')
    timestamp = datetime.datetime.now().timestamp()
    timestamp = str(int(timestamp))
    idCard = str(id_card)
    deviceNo = 'kkb-test-001'
    position = '(116.308015,39.819311)'
    ip = '59.110.157.244'
    mac ='00:16:3e:2e:15:0e'
    # 按照固定顺序生成sign
    params = ['secret','nonce_str','timestamp','idCard','deviceNo','position','ip','mac']
    pre_sign = 'appId='+appid
    for p in params:
        pre_sign+='&'+p+'='+eval(p)
    print(pre_sign)
    md = hashlib.md5()
    md.update(pre_sign.encode('utf-8'))
    sign = md.hexdigest().upper()
    print(sign)

    data={
        'idCard':id_card,
        'deviceNo':deviceNo,
        'position':position,
        'ip':ip,
        'mac':mac,
        'nonce_str':nonce_str,
        'timestamp':timestamp,
        'sign':sign,
        'appId':appid
    }
    rsp = requests.post(url,data=data).json()
    print(rsp)
    if rsp.get('code')=='200':
        color = rsp.get('data').get('color')
        green_status=['0','10','20','30','31','41']
        un_register_status = ['21', '88', '']
        if color in green_status:
            return '绿色'
        elif color=='1':
            return  '黄色'
        elif color in un_register_status:
            return '未在健康宝注册'
        elif color =='2':
            return '红色'
    else:
        return rsp.get('message')







if __name__ == '__main__':
    id_card = '362526199709150010'
    print(get_student_status(id_card))




