from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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