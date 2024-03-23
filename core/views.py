from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import *
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.


class SignupEmployee(CreateView):
    model = User
    form_class = SignupEmployee
    template_name = 'signupEmployee.html'

    def form_valid(self, form):
        user = form.save()
        return redirect('loginEmployee')


class SignupResident(CreateView):
    model = User
    form_class = SignupResident
    template_name = 'signupresident.html'


    def form_valid(self, form):
         user = form.save()
         return redirect('loginResident')


def login_Employeepage(request):
    if request.method == "GET":
        return render(request,'loginEmployee.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            print("wrong username or password")
            return redirect('loginEmployee')


def login_Resident(request):
    if request.method == "GET":
        return render(request,'loginResident.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            print("wrong username or password")
            return redirect('loginResident')




@login_required()
def homepage(request):
    return render(request,'homepage.html')

