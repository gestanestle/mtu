from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
class Student (models.Model):
    student_no = models.CharField(primary_key=True, max_length=11)

class Student_Record (models.Model):
    student_no = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    course = models.CharField(max_length=50)
    year_level = models.IntegerField(default=1)
    current_SY = models.CharField(max_length=9)
    current_sem = models.CharField(max_length=20)


class UserManager(BaseUserManager):
    def create_user(self, student_no, user_name, email, password, **other_fields):
        if email is None:
            raise TypeError('Users must have an email address.')
            
        user = self.model(student_no=student_no, user_name=user_name, email=self.normalize_email(email), password=password, **other_fields)

        user.set_password(password)
        user.save()
        return user

    
    def create_superuser(self, student_no, user_name, email, password, **other_fields):

        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        return self.create_user(student_no, user_name, email, password, **other_fields) 

class User(AbstractBaseUser, PermissionsMixin):
    student_no = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    user_name = models.CharField(max_length=20, default=student_no, unique=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=500, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ['student_no', 'email', 'password']

    def __str__ (self):
        return self.user_name
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    objects = UserManager()



   
    
