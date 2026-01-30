from django.contrib import admin
from .models import Memo

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'confidence', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content', 'keywords']
