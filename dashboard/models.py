from django.views import View
from django.db import models
from about.models import *

class DashboardAboutItem(models.Model):
    category = models.ForeignKey(
        MainCategory,  # aboutアプリのモデルを参照
        on_delete=models.CASCADE,
        related_name='dashboard_items'
    )

# class DashboardBlogItem(models.Model):
#     category = models.ForeignKey(
        
#     )