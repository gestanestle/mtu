from atexit import register
from django.contrib import admin
from .models import Student, Student_Record, User
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(Student)
admin.site.register(Student_Record)
admin.site.register(User)
admin.site.register(AuthUser, UserAdmin)
# Register your models here.
