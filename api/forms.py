from .models import Student, Student_Record
from django import forms
from django.forms import fields

class Student_Record_Form(forms.Form):
    class Meta:
        model = Student_Record 
        fields = "__all__"

