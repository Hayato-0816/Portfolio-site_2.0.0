from django.db import models

class Message(models.Model):
    CATEGORYS = (
        ('request', 'ご依頼'),
        ('consultation', 'ご相談'),
        ('inquiry', 'お問い合わせ'),
        ('other', 'その他'),
    )

    company_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    category = models.CharField(
        max_length=30,
        choices=CATEGORYS,
        default='other'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
