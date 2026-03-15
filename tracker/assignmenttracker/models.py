from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects', null=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    days = models.CharField(max_length=50) # Removed placeholder
    time = models.TimeField() 

    def __str__(self):
        return f"{self.code} - {self.name}"

class Assignment(models.Model):
    CATEGORY_CHOICES = [
        ('PROJECT', 'Project'),
        ('ASSIGNMENT', 'Assignment'),
        ('GROUPWORK', 'Groupwork'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assignments')
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ASSIGNMENT')
    is_major = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    # ... any other fields you have