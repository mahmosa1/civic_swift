from django.views.generic.edit import CreateView
from .forms import SignupForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login

# Create your views here.

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'signup.html'

def form_valid(self, form):
    user = form.save()
    return redirect('profile')

def login_page(request):
    if request.method == "GET":
        return render(request,'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
            print("wrong username or password")
            return redirect('login')


@login_required()
def profile(request):
    return HttpResponse("<h1 only authenticated users can see this page")
