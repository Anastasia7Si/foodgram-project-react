from django.contrib import admin

from .models import User, Following


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
