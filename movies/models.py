from django.db import models
import re
import bcrypt
# Create your models here.

EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "User first name should be more than 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "User last name should be more than 2 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "This email is invalid"

        if len(postData['password']) < 8:
            errors["password"] = "This password  is invalid"

        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "This password  is invalid"

        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "This email is already registered!"

        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['password']) < 8:
            errors["password"] = "This password  is invalid"

        if len(User.objects.filter(email=postData['email'])) < 1:
            errors['email'] = "This email is invalid!"

            return errors


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    # release_date = models.DateTimeField(blank=True)
    run_time = models.CharField(max_length=255)
    poster = models.CharField(max_length=255, default='salam')
    created_at = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movies = models.ManyToManyField(Movie, related_name="users")
    objects = UserManager()
