import random
import json
import http.client
import urllib.parse

from django.core.cache import cache

from swiper import config
from common import keys
from worker import celery_app


def gen_vcode(size=4):
    start = 10 ** (size-1)
    end = 10 ** size - 1
    return str(random.randint(start, end))


@celery_app.task
def send_sms(phone):
    vcode = gen_vcode()
    print(vcode)
    cache.set(keys.VCODE_KEY % phone, vcode, timeout=120)
    result = {'code': 2, 'msg': '提交成功', 'smsid': '15984443354038494607'}
    if result['code'] == 2:
        return True, 'OK'
    else:
        return False, result['msg']


def send_sms_true(phone):
    params = config.HY_PARAMS.copy()
    params['mobile'] = phone
    params['content'] = f'您的验证码是：{gen_vcode()}。请不要把验证码泄露给其他人。'
    params = urllib.parse.urlencode(params)

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    conn = http.client.HTTPConnection(config.HY_host, port=80, timeout=30)
    conn.request("POST", config.HY_sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = json.loads(response.read())
    conn.close()

    """
    if 判断 服务器 是否有反应:
        if response_str.get('code') == 2:
            return True, "OK"
        else:
            return False, response_str['msg']
    else:
        return False, '访问短信服务器有误'
    """

    return response_str









