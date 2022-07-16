from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(OriginalUserAdmin):
    pass

