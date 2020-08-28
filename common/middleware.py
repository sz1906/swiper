from django.utils.deprecation import MiddlewareMixin

from user.models import User
from lib.http import render_json
from common import errors

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 白名单安排，白名单内的地址，直接返回
        white_list = ['/api/user/submit/phone/',
                      '/api/user/submit/vcode/']
        if request.path in white_list:
            return None

        # 判断 request 的 session 中是否存在uid，若存在，说明已登录
        # 不存在，则未登录，提示
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED, data='请登录')
        # 如果已登录，则把 user 写入 request
        user = User.objects.get(id=uid)
        request.user = user
