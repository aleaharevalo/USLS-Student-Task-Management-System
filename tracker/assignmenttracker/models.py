from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=100) # e.g., "Ethics"
    
    def __str__(self):
        return self.name

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    is_major = models.BooleanField(default=False) # Major Project vs Minor Activity
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title}"