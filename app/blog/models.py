from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import jaconv

# Tools ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def japanese_slugify(text):
    # 日本語をローマ字に変換してからスラッグ化
    romaji = jaconv.kana2alphabet(jaconv.hira2kata(jaconv.z2h(text)))
    return slugify(romaji)


class BlogImage(models.Model):
    image = models.ImageField(upload_to='blog_images/%Y/%m/%d/')

# Category ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = japanese_slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Post ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', '下書き'),
        ('published', '公開'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='published_date', blank=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts',
    )
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
    )
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog_images/%Y/%m/%d/',
        blank=True
    )
    published_date = models.DateTimeField('公開日', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
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
        # 1. タイトルが空の場合の処理
        if not self.title:
            self.title = "untitled"
        
        # 2. スラッグが空の場合の処理
        if not self.slug:
            self.slug = japanese_slugify(self.title)  # タイトルからスラッグを生成
            if not self.slug:  # スラッグ生成が失敗した場合
                self.slug = "untitled"
            self.save()  # 生成したスラッグを保存

        # 3. 日付の処理（現在は使用していない）
        date_to_use = self.published_date or self.created_date
        if not date_to_use:
            from django.utils import timezone
            date_to_use = timezone.now()

        # 4. URLの生成
        return reverse('blog:post_detail', args=[
            self.slug,  # URLにスラッグのみを使用
        ])
