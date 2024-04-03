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
    path('EmployeeM/', EmployeeM, name='EmployeeM'),
    path('ResidentM/', ResidentM, name='ResidentM'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('admin/', EmployeeM, name='Admin'),
    path('Volunteer/', Volunteer, name='Volunteer'),
    path('aa/', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]