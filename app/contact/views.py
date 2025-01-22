from django.views.generic import *
from .models import *
from django.http import JsonResponse
from django.views.generic import FormView
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

class MessageView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    
    def form_valid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # フォームデータの保存
                contact = form.save()
                
                # 管理者へのメール送信
                # admin_message = f"""
                # 新しいお問い合わせがありました。

                # 会社名: {contact.company_name}
                # お名前: {contact.name}
                # メールアドレス: {contact.email}
                # 電話番号: {contact.phone_number}
                
                # お問い合わせ内容:
                # {contact.message}
                # """
                
                # send_mail(
                #     '新しいお問い合わせ',
                #     admin_message,
                #     settings.DEFAULT_FROM_EMAIL,
                #     [admin[1] for admin in settings.ADMINS],
                #     fail_silently=False,
                # )
                
                # 送信者への自動返信メール
                # user_message = f"""
                # {contact.name} 様
                
                # お問い合わせありがとうございます。
                # 以下の内容で承りました。
                
                # 会社名: {contact.company_name}
                # お名前: {contact.name}
                # メールアドレス: {contact.email}
                # 電話番号: {contact.phone_number}
                
                # お問い合わせ内容:
                # {contact.message}
                
                # 内容を確認次第、担当者よりご連絡させていただきます。
                # """
                
                # send_mail(
                #     'お問い合わせを受け付けました',
                #     user_message,
                #     settings.DEFAULT_FROM_EMAIL,
                #     [contact.email],
                #     fail_silently=False,
                # )
                
                return JsonResponse({'status': 'success'})
                
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            })
        return super().form_invalid(form)