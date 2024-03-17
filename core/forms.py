from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import path



class SignupEmployee(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class SignupResident(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']