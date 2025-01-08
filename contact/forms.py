from django import forms
from .models import Message

class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['company_name', 'name', 'email', 'phone_number', 'message']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and len(email) > 254:
            raise forms.ValidationError('メールアドレスは254文字以内で入力してください。')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            import re
            if not re.match(r'^[0-9-]{10,13}$', phone):
                raise forms.ValidationError('電話番号は10桁から13桁の数字とハイフンで入力してください。')
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            raise forms.ValidationError('お名前は100文字以内で入力してください。')
        return name