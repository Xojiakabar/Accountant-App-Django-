from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'image']
    search_fields = ['username']
    list_editable = ['is_active']
    ordering = ['is_active']

# admin.site.register(UserAdmin)