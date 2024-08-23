from django.contrib import admin
from .models import BaseUser


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email"]
    list_per_page = 10
    search_fields = ["full_name", "email"]
    search_help_text = "Enter full name or email to find user"
