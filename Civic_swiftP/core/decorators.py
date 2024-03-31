from django .http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required

def Resident_limit(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Resident').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this page.")
    return wrapper

def Employee_limit(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Employee').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this page.")
    return wrapper

def admin_limit(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this page.")
    return wrapper