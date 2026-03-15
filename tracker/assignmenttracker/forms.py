from django import forms
from .models import Task

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'subject', 'due_date', 'category', 'is_major']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border-b-2 border-gray-200 focus:border-green-600 outline-none py-2 text-lg font-bold placeholder-gray-300',
                'placeholder': 'e.g., Final Capstone Documentation'
            }),
            'subject': forms.Select(attrs={
                'class': 'w-full border-b-2 border-gray-200 focus:border-green-600 outline-none py-2 font-bold bg-white'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border-b-2 border-gray-200 focus:border-green-600 outline-none py-2 font-bold bg-white'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'w-full border-b-2 border-gray-200 focus:border-green-600 outline-none py-2 font-bold',
                'type': 'datetime-local'
            }),
            'is_major': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-500'
            }),
        }