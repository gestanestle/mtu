from atexit import register
from django.contrib import admin
from .models import Student, Student_Record, User

admin.site.register(Student)
admin.site.register(Student_Record)
admin.site.register(User)
# Register your models here.
