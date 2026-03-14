from django.shortcuts import render, redirect
from .models import Assignment
from .forms import AssignmentForm

# THE DASHBOARD (View Only)
def dashboard(request):
    assignments = Assignment.objects.all().order_by('due_date')
    return render(request, 'assignmenttracker/dashboard.html', {
        'assignments': assignments
    })

# THE ADD FORM (Create Only)
def add_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # Go back to dashboard after saving
    else:
        form = AssignmentForm()
    
    return render(request, 'assignmenttracker/add_assignment.html', {'form': form})