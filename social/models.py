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



