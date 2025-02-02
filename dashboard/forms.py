from django import forms
from app.about.models import *

class AboutMainCategoryForm(forms.ModelForm):
    class Meta:
        model = AboutMainCategory
        fields = ['name', 'icon_image', 'order', 'is_active']

class AboutSubCategoryForm(forms.ModelForm):
    class Meta:
        model = AboutSubCategory
        fields = ['name', 'order', 'is_active']

class AboutSkillForm(forms.ModelForm):
    class Meta:
        model = AboutSkill
        fields = ['name', 'order', 'is_active']
