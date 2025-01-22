from django.db import models

class ContactMessage(models.Model):
    CATEGORYS = (
        ('request', 'ご依頼'),
        ('consultation', 'ご相談'),
        ('inquiry', 'お問い合わせ'),
        ('other', 'その他'),
    )

    company_name = models.CharField("会社名", max_length=100, blank=True)
    name = models.CharField("お名前", max_length=100)
    email = models.EmailField("メールアドレス")
    phone_number = models.CharField("電話番号", max_length=100)
    category = models.CharField(
        "カテゴリ",
        max_length=30,
        choices=CATEGORYS,
        default='other',
        blank=True,
    )
    message = models.TextField("お問い合わせ内容")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
