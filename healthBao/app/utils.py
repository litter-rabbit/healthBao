
import requests
import logging
from django.utils.deprecation import MiddlewareMixin
logger = logging.getLogger()


class ExceptionLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        import traceback
        logger.error(traceback.format_exc())


def get_student_status(id_card):
    url='https://jiankangapi.capcloud.com.cn/api/query/healthyQueryV3'

    data={
        'idCard':id_card,
        'deviceNo':'kkb001',
        'position':'(116.308015,39.819311)',
        'ip':'59.110.157.244',
        'mac':'00:16:3e:2e:15:0e'
    }

    rsp = requests.post(url,data=data).json()

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
        return 'error'





if __name__ == '__main__':
    id_card = '362526199709150010'
    get_student_status(id_card)




