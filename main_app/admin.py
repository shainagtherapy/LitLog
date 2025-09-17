from django.contrib import admin
from .models import Log
from .models import Profile

# Register your models here.
admin.site.register(Log)
admin.site.register(Profile)
