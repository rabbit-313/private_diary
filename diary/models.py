from accounts.models import CustomUser
from django.db import models


class Diary(models.Model):
    """日記モデル"""

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    api_key = models.CharField(verbose_name='ChatGPTのAPI-key', max_length=40, null=False)
    event1 = models.TextField(verbose_name='出来事', blank=True, null=True)
    # event2 = models.CharField(verbose_name='出来事2', max_length=40, blank=True, null=True)
    # event3 = models.CharField(verbose_name='出来事3', max_length=40, blank=True, null=True)
    # event4 = models.CharField(verbose_name='出来事4', max_length=40, blank=True, null=True)
    # event5 = models.CharField(verbose_name='出来事5', max_length=40, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Diary'

    def __str__(self):
        return self.title
