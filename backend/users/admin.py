from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Follow


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', ]
    list_filter = ['email', 'username', ]


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
