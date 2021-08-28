from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        
        errors={}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters."
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "Must enter an email."
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must enter an valid email."
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "Email already registered."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long."
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Password do not match."
        return errors

    def login_validator(self, postData):
        errors={}
        registered_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Must enter an email."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long."
        elif bcrypt.checkpw(postData['password'].encode(), registered_user[0].password.encode()) !=True:
            errors['password'] = "Email and Password do not match."



class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()