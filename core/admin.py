from django.contrib import admin
from core.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
