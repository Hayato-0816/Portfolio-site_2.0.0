from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField('カテゴリー名', max_length=100)
    slug = models.SlugField('スラッグ', unique=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    class Meta:
        verbose_name = 'Category'          # 管理画面での単数形の表示名
        verbose_name_plural = 'Category'   # 管理画面での複数形の表示名
        ordering = ['name']                # データの取得順序（nameフィールドで昇順

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gallery:category_detail', kwargs={'slug': self.slug})

class GalleryItem(models.Model):
    title = models.CharField('タイトル', max_length=200)
    description = models.TextField('説明', blank=True)
    image = models.ImageField('画像', upload_to='gallery/%Y/%m/%d/')
    category = models.ForeignKey(
        Category,
        verbose_name='Category',
        on_delete=models.PROTECT,
        related_name='items'
    )
    url = models.URLField('URL', blank=True)
    is_public = models.BooleanField('公開する', default=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        verbose_name = 'Gallery Item'
        verbose_name_plural = 'Gallery Item'
        ordering = ['-created_at']         # データの取得順序（created_atフィールドで降順）

    def get_absolute_url(self):
        return reverse('gallery:item_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title