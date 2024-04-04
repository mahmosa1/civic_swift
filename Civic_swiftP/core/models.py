from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add more fields as needed for Employee profile

    def _str_(self):
        return self.user.username


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add more fields as needed for Resident profile

    def _str_(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.TextField(max_length=600,null=False)
    date_created = models.DateTimeField(auto_now_add=True,null=False)

    def _str_(self):
        return self.caption