from django.db import models


class Swiped(models.Model):
    MARK = (
        ('like', 'like'),
        ('superlike', 'superlike'),
        ('dislike', 'dislike')
    )
    uid = models.IntegerField(verbose_name='用户自身ID')
    sid = models.IntegerField(verbose_name='被滑的陌生人ID')
    mark = models.CharField(choices=MARK, verbose_name='滑动类型', max_length=16)
    time = models.DateTimeField(verbose_name='滑动的时间', auto_now_add=True)

    class Meta:
        db_table = 'swiped'

    @classmethod
    def like(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='like')

    @classmethod
    def has_like(cls, uid, sid):
        return cls.objects.filter(uid=sid, sid=uid).exists()

    @classmethod
    def dislike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='dislike')

    @classmethod
    def superlike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='supermark')


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        friendship = cls.objects.create(uid1=uid1, uid2=uid2)
        return friendship

    @classmethod
    def is_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return Friend.objects.filter(uid1=uid1, uid2=uid2).exclude()

    @classmethod
    def delete_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return Friend.objects.filter(uid1=uid1, uid2=uid2).delete()
