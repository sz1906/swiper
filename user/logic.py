from django.conf import settings
import os

from common import keys
from lib.qiniuyun import upload_qiniu
from swiper import config


def handle_upload(user, avatar):
    filename = keys.AVATAR_KEY % user.id  # AVATAR-1
    file_path = os.path.join(settings.BASE_DIR, settings.MEDIAS, filename)
    with open(file_path, mode='ab') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)

    # 上传到七牛云
    upload_qiniu(user, file_path)
    user.avatar = config.QINIU_URL + filename
    user.save()
