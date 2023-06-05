import datetime
from django.shortcuts import render, redirect
from django import forms
from .models import Tasks
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

last_login = []
completed_tasks = []
# Create your views here.
def index(request):
    return render(request, 'TODO_app/index.html')

def signup_user(request):
    #getting credentials from the user i.e front end if the condition is true
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_password = request.POST.get('user_password')
        user_password_repeat = request.POST.get('user_password_repeat')
        # checking all the basic conditions for user sign up
        try:
            if len(user_password) >= 8:
                if user_password == user_password_repeat and len(user_name) >= 3:
                    user = User.objects.create_user(
                        username=user_name,
                        email=user_email,
                        password=user_password,
                    )
                    user.last_login = datetime.datetime.now()
                    user.save()
                    return redirect('/login')

                else:
                    #sending warnings according to the condition met
                    error_message = "Username is too short or password didn't match, Try resolving these mistakes!!"
                    return render(request, 'TODO_app/index.html', {'error_message': error_message})
            else:
                error_message = "Password should contain at least 8 characters"
                return render(request, 'TODO_app/index.html', {'error_message': error_message})

        except:
            error_message = "username already exists, Try with the different one!!"
            return render(request, 'TODO_app/index.html', {'error_message': error_message})


def login_user(request):
    #getting credentials for the login
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        # checking is the user has an account or not
        is_user = authenticate(request, username=user_name, password=user_password)
        #if he have an account then
        if is_user is not None:
            login(request, is_user)
            return redirect('/tasks_list')
        #if he have'nt or hit the wrong credentials
        else:
            error_message = "username or password is invalid, Please try with the valid one!!"
            return render(request, 'TODO_app/login.html', {'error_message': error_message})

    return render(request, 'TODO_app/login.html')


def logout_user(request):
    #logging out the user and redirecting them to login page
    logout(request)
    return redirect('/login')


class TaskDetail(LoginRequiredMixin, DetailView):
    # this is model
    model = Tasks
    # this is parameter (model) as tasks_details name to show the task with description and other details
    context_object_name = 'tasks_details'
    template_name = 'TODO_app/task.html'


class TaskList(LoginRequiredMixin, ListView):
    # this is model
    model = Tasks
    # this is parameter which shows all the tasks
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #to filer the tasks with respect to the user only
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Tasks
    #these are the fileds that will visible from the front end
    fields = ['title', 'description', 'tag', 'status', 'due_date']
    template_name = 'TODO_app/task_create.html'
    success_url = reverse_lazy('tasks_list')
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # to change the format of the date, because by django it was set as text
        form.fields['due_date'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        # to add current time in the created_on field
        form.instance.user = self.request.user
        form.instance.created_on = datetime.datetime.now()
        #logic so that a user can't put the due date before the current date
        due_date = form.cleaned_data['due_date']
        c_time = datetime.datetime.now(datetime.timezone.utc)
        if due_date < c_time:
            form.add_error('due_date', 'Due date must be greater than current date.')
            return self.form_invalid(form)
        return super(TaskCreate, self).form_valid(form)



class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Tasks
    fields = ['title', 'description', 'tag', 'status', 'due_date']
    template_name = 'TODO_app/task_form.html'
    success_url = reverse_lazy('tasks_list')
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        due_date = form.cleaned_data['due_date']
        c_time = datetime.datetime.now(datetime.timezone.utc)
        if due_date < c_time:
            form.add_error('due_date', 'Due date must be greater than current date.')
            return self.form_invalid(form)
        return super(TaskUpdate, self).form_valid(form)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Tasks
    context_object_name = 'task'
    # to redirect to another page after the success of one deletion
    success_url = reverse_lazy('tasks_list')


