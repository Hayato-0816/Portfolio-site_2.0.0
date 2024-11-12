from django import forms
from blog.models import Category, Post

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # slugは自動生成されるので除外

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'status', 'featured_image']  # 必要なフィールドを指定
        exclude = ['author', 'slug']  # 自動的に設定されるフィールドを除外

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)