from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import path
from.models import Message, ResidentMessage
from django.forms import ModelForm
from django import forms



class SignupEmployee(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class SignupResident(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class MessageForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'input'}))

    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']



class ReportProblemForm(forms.ModelForm):
    class Meta:
        model = ResidentMessage
        fields = ['subject', 'message']


