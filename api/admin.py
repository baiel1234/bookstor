from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author')
