from django.contrib import admin
from user_app.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
