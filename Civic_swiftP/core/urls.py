from django.contrib import admin
from django.urls import path , include
from .views import *
from . import views
urlpatterns = [
    path('signupresident/', SignupResident.as_view(),name='signupresident'),
    path('signupEmployee/', SignupEmployee.as_view(),name='signupEmployee'),
    path('logout/',logout_user,name='logout'),
    path('loginEmployee/',login_Employeepage,name='loginEmployee'),
    path('loginResident/',login_Resident,name='loginResident'),
    path('',homepage,name='homepage'),
    path('search',views.search,name='search'),

]