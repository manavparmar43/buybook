from email.policy import default
from django.db import models

from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email,  username, password=None,**extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None,**extra_fields):

        print('-------',extra_fields)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_student', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError((
                'Super user must have is_staff'
            ))

        return self.create_user(email,username,password,**extra_fields)


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
   
    created_at = models.DateTimeField(default=datetime.now(tz=timezone.utc))
    updated_at = models.DateTimeField(default=datetime.now(tz=timezone.utc))
    is_student=models.BooleanField()
    phone=models.CharField(max_length=10)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email





class Book(models.Model):
    bookname=models.CharField(max_length=200)
    bookprice=models.IntegerField()
    bookpage = models.IntegerField()
    authername=models.CharField(max_length=300)
    booklanguage = models.CharField(max_length=300)
    bookquantity=models.CharField(max_length=10)
    deleted= models.BooleanField(default=False)


    def __str__(self):
        return self.bookname

class Buybook(models.Model):
    bookdetail=models.ForeignKey(Book,null=True, on_delete=models.SET_NULL)
    username=models.CharField(max_length=150)
    buydate=models.DateField()
    returndate=models.DateField()
    buybookquantity = models.CharField(max_length=10)
    buy=models.BooleanField()
    phone=models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username




