from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import *
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import Group
from .decorators import *
from .models import Employee, Resident
# Create your views here.


class SignupEmployee(CreateView):
    model = User
    form_class = SignupEmployee
    template_name = 'signupEmployee.html'

    def form_valid(self, form):
        user = form.save()
        Employee_group = Group.objects.get(name='Employee')
        Employee_group.user_set.add(user)
        return redirect('homepage')


class SignupResident(CreateView):
    model = User
    form_class = SignupResident
    template_name = 'signupresident.html'


    def form_valid(self, form):
         user = form.save()
         Resident_group = Group.objects.get(name='Resident')
         Resident_group.user_set.add(user)
         return redirect('homepage')


def login_Employeepage(request):
    if request.method == "GET":
        return render(request,'loginEmployee.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('EmployeeM')
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
            return redirect('ResidentM')
        else:
            print("wrong username or password")
            return redirect('loginResident')

def logout_user(request):
    logout(request)
    return redirect('loginEmployee')



def homepage(request):
    return render(request,'homepage.html')

@login_required
@Employee_limit
def EmployeeM(request):
    return render(request,'EmployeeM.html')

@login_required
@Resident_limit
def ResidentM(request):
    return render(request,'ResidentM.html')

def search(request):
    query = request.GET.get('query', '').strip().lower()
    if not query:
        # No search query was entered
        return HttpResponse("You did not search for anything.")

    # Define a mapping of keywords to view names (URL names)
    search_mappings = {

    }


    for keyword, view_name in search_mappings.items():
        if query == keyword:

            return redirect(reverse(view_name))


    return HttpResponse(f"No results found for '{query}'.")

def Volunteer(request):
    return render(request, 'Volunteer.html')