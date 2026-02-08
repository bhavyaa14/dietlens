from django.contrib import admin

# Register your models here.

from diet_advisor.models import UserProfile

admin.site.register(UserProfile)