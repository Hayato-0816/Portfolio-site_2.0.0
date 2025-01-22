from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField('自己紹介', max_length=500, blank=True)
    profile_image = models.ImageField(
        'プロフィール画像',
        upload_to='profile_pics/',
        blank=True
    )

    def __str__(self):
        return f'{self.user.username}のプロフィール'

class AboutMainCategory(models.Model):
    name = models.CharField('カテゴリー名', max_length=100)
    title_ja = models.CharField('日本語名', max_length=100)
    order = models.IntegerField('表示順', default=0)
    is_active = models.BooleanField('有効', default=True)

    def __str__(self):
        return self.title_ja

class AboutSubCategory(models.Model):
    main_category = models.ForeignKey(
        AboutMainCategory,
        on_delete=models.CASCADE,
        related_name='sub_categories'
    )
    name = models.CharField('カテゴリー名', max_length=100)
    title_ja = models.CharField('日本語名', max_length=100)
    order = models.IntegerField('表示順', default=0)
    is_active = models.BooleanField('有効', default=True)

    def __str__(self):
        return f'{self.main_category.title_ja} - {self.title_ja}'

class AboutSkill(models.Model):
    sub_category = models.ForeignKey(
        AboutSubCategory,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField('スキル名', max_length=100)
    description = models.TextField('説明', blank=True)
    order = models.IntegerField('表示順', default=0)
    is_active = models.BooleanField('有効', default=True)

    def __str__(self):
        return self.name