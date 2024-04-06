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
    path('Volunteer/', Volunteer.as_view(), name='Volunteer'),
    path('new-post/',CreatPost.as_view(),name='new-post'),
    path('inbox/', views.inbox, name="inbox"),
    path('send-message/', views.createMessage, name='create-message'),
    path('report-problem/', CreateProblemReport.as_view(), name='report_problem'),
    path('problem-reports/', view_problem_reports, name='problem_reports'),


]