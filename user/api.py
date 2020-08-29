from django.shortcuts import render
from django.core.cache import cache

from user.forms import ProfileModelForm
from user.models import User
from lib.sms import send_sms
from common import errors
from lib.http import render_json
from common import keys
from user.logic import handle_upload


def submit_phone(request):
    """提交手机号码，发送验证码"""
    phone = request.POST.get('phone')
    # 发送验证码
    send_sms.delay(phone)
    return render_json()


def submit_vcode(request):
    """提交短信验证码"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    # 从缓存中取出 vcode
    cached_vcode = cache.get(keys.VCODE_KEY % phone)
    if vcode == cached_vcode:
        # 验证码正确，可登录或注册
        user, _ = User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})
        # 把用户ID存入session中，完成登录
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    return render_json(data=request.user.profile.to_dict())


def edit_profile(request):
    """修改个人资料"""
    form = ProfileModelForm(request.POST)
    if form.is_valid():
        # 可以接收并保存
        profile = form.save(commit=False)  # 先不保存
        uid = request.user.id
        profile.id = uid
        profile.save()
        return render_json(data=profile.to_dict())
    return render_json(code=errors.PROFILE_ERROR, data=form.errors)


def upload_avatar(request):
    avatar = request.FILES.get('avatar')
    user = request.user
    handle_upload.delay(user, avatar)
    return render_json()

