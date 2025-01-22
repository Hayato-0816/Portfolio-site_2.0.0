from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

class AboutSubCategoryInline(admin.TabularInline):
    model = AboutSubCategory
    extra = 1

class AboutSkillInline(admin.TabularInline):
    model = AboutSkill
    extra = 1

@admin.register(AboutMainCategory)
class AboutMainCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_ja', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [AboutSubCategoryInline]

@admin.register(AboutSubCategory)
class AboutSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_ja', 'main_category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('main_category', 'is_active')
    inlines = [AboutSkillInline]

@admin.register(AboutSkill)
class AboutSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('sub_category__main_category', 'sub_category', 'is_active')