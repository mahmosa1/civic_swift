from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add more fields as needed for Employee profile

    def __str__(self):
        return self.user.username


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add more fields as needed for Resident profile

    def __str__(self):
        return self.user.username
