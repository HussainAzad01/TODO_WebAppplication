import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateTimeInput

# Create your models here.
class Tasks(models.Model):
    choices = [('OPEN', 'Open'),
               ('WORKING', 'Working'),
               ('DONE', 'Done'),
               ('OVERDUE', 'Overdue')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=False, default="COMPLETE TASKS")
    tag = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=choices, default='OPEN', null=False, blank=False)
    due_date = models.DateTimeField(null=True, blank=True)
    created_on = models.DateField()

    def __str__(self):
        return self.title


