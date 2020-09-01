import datetime

from django.core.cache import cache
from django.db.models import Q

from swiper import config
from common import keys, errors
from lib.http import render_json
from social import logic
from social.models import Swiped, Friend
from user.models import User


def get_recd_list(request):
    """获取推荐列表"""
    user = request.user
    data = logic.get_recd_list(user)
    return render_json(data=data)


def like(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.like(user.id, sid)
    return render_json(data={'match': flag})


def dislike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.dislike(user.id, sid)
    return render_json(data={'unmatch': flag})


def superlike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.superlike(user.id, sid)
    return render_json(data={'match': flag})


def rewind(request):
    """
    每天允许反悔三次，反悔次数记录在 redis 中
    每次执行反悔操作时，先判断反悔次数是否小于配置的当天最大反悔次数
    """
    user = request.user
    code, data = logic.rewind(user)
    return render_json(code=code, data=data)


def show_friends(request):
    """查看好友列表"""
    user = request.user
    data = logic.show_friends(user)
    return render_json(data=data)


def show_friends_information(request):
    sid = request.POST.get('sid')
    friend_information = User.objects.filter(id=sid)[0]
    return render_json(data=friend_information.to_dict())

