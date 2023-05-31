from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup_user, name="signup_user"),
    path('login', views.login_user, name="login_user"),
    path('logout', views.logout_user, name="logout_user"),
    path('tasks_list', TaskList.as_view(), name="tasks_list"),
    path('task/<int:pk>/', TaskDetail.as_view(), name="tasks_detail"),
    path('task_create', TaskCreate.as_view(), name="tasks_create"),
    path('task_update/<int:pk>/', TaskUpdate.as_view(), name="tasks_update"),
    path('task_delete/<int:pk>/', TaskDelete.as_view(), name="tasks_delete"),

]
urlpatterns += staticfiles_urlpatterns()