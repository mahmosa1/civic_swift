from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from .decorators import *
from .models import *
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.

def admin_login(request):
    # Your view logic here
    return render(request, 'admin/login.html')


class SignupEmployee(CreateView):
    model = User
    form_class = SignupEmployee
    template_name = 'signupEmployee.html'

    def form_valid(self, form):
        user = form.save()
        #send_mail(
            #'Welcome to CivicSwift!',
            #'Thank you for signing up.',
            #settings.EMAIL_HOST_USER,
            #[User.email],
            #fail_silently=False,
        #)
        Employee_group = Group.objects.get(name='Employee')
        Employee_group.user_set.add(user)
        return redirect('homepage')


class SignupResident(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        # Create a Resident object for the user
        resident = Resident.objects.create(user=user)
        # Commenting out email sending for now
        # send_mail(
        #     'Welcome to CivicSwift!',
        #     'Thank you for signing up.',
        #     settings.EMAIL_HOST_USER,
        #     [user.email],
        #     fail_silently=False,
        #)

        # Add the user to the "Resident" group
        resident_group = Group.objects.get(name='Resident')
        resident_group.user_set.add(user)

        return user

def signup_resident(request):
    if request.method == 'POST':
        form = SignupResident(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or homepage
            return redirect('homepage')
    else:
        form = SignupResident()
    return render(request, 'signupresident.html', {'form': form})


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
    return redirect('homepage')



def homepage(request):
    return render(request,'homepage.html')

@login_required
@Employee_limit
def EmployeeM(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the selected resident ID from the form data
            resident = form.cleaned_data['resident']
            file = form.cleaned_data['file']

            try:
                # Create and save the UploadedFile instance
                uploaded_file = UploadedFile(resident=resident, file=file)
                uploaded_file.save()

                return redirect('EmployeeM')
            except User.DoesNotExist:
                # Handle the case where resident with given ID does not exist
                return HttpResponse("Selected resident does not exist.")
    else:
        form = UploadFileForm()

    residents = User.objects.filter(groups__name='Residents')  # Filter residents based on group
    return render(request, 'employeeM.html', {'form': form, 'residents': residents})

@login_required
@Resident_limit
def ResidentM(request):
    # Filter uploaded files based on the logged-in resident
    uploaded_files = UploadedFile.objects.filter(resident=request.user)
    return render(request, 'ResidentM.html', {'uploaded_files': uploaded_files})


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


def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('homepage')
    except User.DoesNotExist:
        # Handle the case where the user doesn't exist
        return redirect('homepage')


class CreatPost(CreateView):
    model = Post
    fields = ['caption']
    template_name = "new_post.html"
    success_url = '/EmployeeM/'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)



class Volunteer(ListView):
    model = Post
    template_name = "Volunteer.html"
    paginate_by = 10000

    def get_queryset(self):
        return  Post.objects.all().order_by('-date_created')

@login_required
def inbox(request):
    user = request.user
    messages = Message.objects.filter(recipient=user).order_by('-created')
    context = {'messages': messages}
    return render(request, 'inbox.html', context)


class CreateMessage(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('ResidentM')

    def form_valid(self, form):
        form.instance.sender = self.request.user

        # Get the Employee user
        employee_user = User.objects.filter(groups__name='Employee').first()
        if employee_user:
            form.instance.recipient = employee_user

        # Save the message
        form.save()

        messages.success(self.request, 'Your message was successfully sent!')
        return super().form_valid(form)

def createMessage(request):
    create_message_view = CreateMessage.as_view()
    return create_message_view(request)


class CreateProblemReport(CreateView):
    model = ResidentMessage
    form_class = ReportProblemForm
    template_name = 'report_problem_form.html'
    success_url = reverse_lazy('ResidentM')

    def form_valid(self, form):
        form.instance.resident = self.request.user

        # Save the problem report
        form.save()

        messages.success(self.request, 'Your problem report was successfully submitted!')
        return super().form_valid(form)

def view_problem_reports(request):

    # Retrieve all problem reports
    problem_reports = ResidentMessage.objects.all()

    context = {
        'problem_reports': problem_reports}
    return render(request, 'problem_reports.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            resident_id = form.cleaned_data['resident']
            file = form.cleaned_data['file']

            try:
                # Retrieve the Resident instance
                resident = User.objects.get(id=resident_id)

                # Create and save the UploadedFile instance
                uploaded_file = UploadedFile(resident=resident, file=file)
                uploaded_file.save()

                return redirect('EmployeeM')
            except User.DoesNotExist:
                # Handle the case where resident with given ID does not exist
                return HttpResponse("Selected resident does not exist.")
    else:
        form = UploadFileForm()

    residents = User.objects.filter(groups__name='Residents')  # Filter residents based on group
    return render(request, 'employeeM.html', {'form': form, 'residents': residents})