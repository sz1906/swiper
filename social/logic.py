import datetime

from django.core.cache import cache
from django.db.models import Q

from user.models import User
from .models import Swiped
from .models import Friend
from common import keys, errors
from swiper import config


def get_recd_list(user):
    # 注意事项：1、已滑过的人，不应再出现；
    # 2、不能出现自己；3、只推荐符合交友资料的用户

    # 根据最大和最小的交友年龄计算对方的出身年份
    now = datetime.datetime.now()
    max_birth_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age

    # 查询已经被当前用户滑过的人
    swiped_list = Swiped.objects.filter(uid=user.id).only('sid')
    # 取出sid
    sid_list = [s.sid for s in swiped_list]
    sid_list.append(user.id)
    users = User.objects.filter(location=user.profile.location,
                                birth_year__range=(min_birth_year, max_birth_year),
                                sex=user.profile.dating_sex).exclude(
        id__in=swiped_list)[:20]
    data = [user.to_dict() for user in users]
    return data


def like(uid, sid):
    # 创建一条记录
    Swiped.like(uid, sid)
    # 判断对方是否喜欢我们
    if Swiped.has_like(uid, sid):
        # 是则建立好友关系，
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def dislike(uid, sid):
    Swiped.dislike(uid, sid)
    Friend.delete_friend(uid1=uid, uid2=sid)
    return True


def superlike(uid, sid):
    Swiped.superlike(uid, sid)
    if Swiped.has_like(uid, sid):
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def rewind(user):
    # 先从缓存中获取当天已反悔次数
    key = keys.REWIND_KEY % user.id
    cached_rewinded_times = cache.get(key, 0)
    if cached_rewinded_times < config.MAX_REWIND:
        # 说明当天还有反悔机会
        # 缓存内反悔次数加1
        cached_rewinded_times += 1
        now = datetime.datetime.now()
        left_seconds = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
        cache.set(key, cached_rewinded_times, timeout=left_seconds)
        # 删除swiped最近的一条记录
        try:
            record = Swiped.objects.filter(uid=user.id).latest('time')
            # 如果有好友关系，解除
            Friend.delete_friend(uid1=user.id, uid2=record.sid)
            record.delete()
            return True, 'ok'
        except Swiped.DoesNotExist:
            cached_rewinded_times -= 1
            cache.set(key, cached_rewinded_times, timeout=left_seconds)
            # return render_json(code=errors.NO_RECORD, data='无操作记录，无法反悔')
            raise errors.NoRecord
    else:

        # return render_json(code=errors.EXCEED_MAXIMUM_REWIND, data='超过最大反悔次数')
        # return errors.EXCEED_MAXIMUM_REWIND, '超过最大反悔次数'
        raise errors.ExceedMaximumRewind

def show_friends(user):
    friends = Friend.objects.filter(Q(uid1=user.id) | Q(uid2=user.id))
    friends_id = []
    for friend in friends:
        if friend.uid1 == user.id:
            friends_id.append(friend.uid2)
        else:
            friends_id.append(friend.uid1)
        # 不建议使用列表推导式，可读性太差
        # [friends_id.append(friend.uid2) if friend.uid1 == user.id else friends_id.append(friend.uid1) for friend in
        #  friends]

    users = User.objects.filter(id__in=friends_id)
    data = [user.to_dict() for user in users]
    return data


