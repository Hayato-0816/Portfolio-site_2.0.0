from django.contrib import admin
from .models import Profile, MainCategory, SubCategory, Skill

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_ja', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [SubCategoryInline]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_ja', 'main_category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('main_category', 'is_active')
    inlines = [SkillInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('sub_category__main_category', 'sub_category', 'is_active')