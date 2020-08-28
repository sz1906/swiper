from qiniu import Auth, put_file, etag

from swiper import config
from common import keys


def upload_qiniu(user, file_path):
    q = Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)

    bucket_name = 'my-swiper-pro'
    filename = keys.AVATAR_KEY % user.id

    token = q.upload_token(bucket_name, filename, 3600)
    ret, info = put_file(token, filename, file_path)
    print(info)
    print(ret)
    # assert ret['key'] == filename
    # assert ret['hash'] == etag(file_path)

