from .models import Student, Student_Record, User
from django import forms
from django.forms import fields, widgets

class UserChangePassword(forms.Form):
    class Meta:
        model: User
        fields = ('password')

class Student_Record_Form(forms.ModelForm):
    class Meta:
        model = Student_Record 
        fields = "__all__"
        exclude = ('student_no',)

class Upload_Image(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image',]