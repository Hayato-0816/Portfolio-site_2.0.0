from django import forms
from app.blog.models import BlogCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name']  # slugは自動生成されるので除外