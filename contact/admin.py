from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'name', 'email', 'phone_number', 'message', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['company_name', 'name', 'email', 'phone_number', 'message']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
