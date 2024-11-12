from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import jaconv

def japanese_slugify(text):
    # 日本語をローマ字に変換してからスラッグ化
    romaji = jaconv.kana2alphabet(jaconv.hira2kata(jaconv.z2h(text)))
    return slugify(romaji)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # blank=Trueを追加
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = japanese_slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '下書き'),
        ('published', '公開'),
    )
    
    title = models.CharField('タイトル', max_length=200)
    slug = models.SlugField('スラッグ', unique_for_date='published_date', blank=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts',
        verbose_name='投稿者'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='カテゴリー'
    )
    content = models.TextField('本文')
    featured_image = models.ImageField(
        'アイキャッチ画像',
        upload_to='blog_images/%Y/%m/%d/',
        blank=True
    )
    published_date = models.DateTimeField('公開日', null=True, blank=True)
    created_date = models.DateTimeField('作成日', auto_now_add=True)
    updated_date = models.DateTimeField('更新日', auto_now=True)
    status = models.CharField(
        '状態',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    class Meta:
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = japanese_slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # タイトルとslugの両方が空の場合のデフォルト値を設定
        if not self.title:
            self.title = "untitled"
        
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
            if not self.slug:  # slugifyの結果が空の場合
                self.slug = "untitled"
            self.save()

        # 日付の処理
        date_to_use = self.published_date or self.created_date
        if not date_to_use:
            from django.utils import timezone
            date_to_use = timezone.now()
        # 公開日が設定されていない場合のフォールバック
        return reverse('blog:post_detail', args=[
            self.created_date.year,
            self.created_date.month,
            self.created_date.day,
            self.slug
        ])