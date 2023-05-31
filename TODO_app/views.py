import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
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
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_password = request.POST.get('user_password')
        user_password_repeat = request.POST.get('user_password_repeat')

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
                    error_message = "Username is too short or password didn't match, Try resolving these mistakes!!"
                    return render(request, 'TODO_app/index.html', {'error_message': error_message})
            else:
                error_message = "Password should contain at least 8 characters"
                return render(request, 'TODO_app/index.html', {'error_message': error_message})

        except:
            error_message = "username already exists, Try with the different one!!"
            return render(request, 'TODO_app/index.html', {'error_message': error_message})


def login_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        is_user = authenticate(request, username=user_name, password=user_password)

        if is_user is not None:
            login(request, is_user)
            return redirect('/tasks_list')
        else:
            error_message = "username or password is invalid, Please try with the valid one!!"
            return render(request, 'TODO_app/login.html', {'error_message': error_message})

    return render(request, 'TODO_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('/login')


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Tasks #this is model
    context_object_name = 'tasks_details' #this is params (model) as tasks_details name
    template_name = 'TODO_app/task.html'


class TaskList(LoginRequiredMixin, ListView):

    model = Tasks  # this is model
    context_object_name = 'tasks'# this is params

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Tasks
    fields = ['title', 'description', 'tag', 'status']
    template_name = 'TODO_app/task_create.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form): #to add current time in the created_on field
        form.instance.user = self.request.user
        form.instance.created_on = datetime.datetime.now()
        return super(TaskCreate, self).form_valid(form)



class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Tasks
    fields = ['title', 'description', 'tag', 'status']
    template_name = 'TODO_app/task_form.html'
    success_url = reverse_lazy('tasks_list')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Tasks
    context_object_name = 'task'
    success_url = reverse_lazy('tasks_list')


