from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    days = models.CharField(max_length=20)  
    start_time = models.TimeField()
    end_time = models.TimeField()
    color = models.CharField(max_length=20, default='bg-green-700')

    def __str__(self):
        return f"{self.code} - {self.name}"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    
    CATEGORY_CHOICES = [
        ('assignment', 'Assignment'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
        ('exam', 'Exam'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_major = models.BooleanField(default=False)

    def __str__(self):
        return self.title