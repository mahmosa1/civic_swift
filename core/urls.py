from django.contrib import admin
from django.urls import path , include
from .views import *
urlpatterns = [
    path('signupresident/', SignupResident.as_view(),name='signupresident'),
    path('signupEmployee/', SignupEmployee.as_view(),name='signupEmployee'),
    path('homepage/',homepage,name='homepage'),
    path('loginEmployee/',login_Employeepage,name='loginEmployee'),
    path('loginResident/',login_Resident,name='loginResident'),


]
