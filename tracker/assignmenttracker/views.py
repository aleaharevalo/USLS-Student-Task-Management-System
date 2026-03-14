from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Assignment
from .forms import AssignmentForm

# --- AUTHENTICATION ---

def login_view(request):
    """Handles student login using the USLS-styled login page."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'assignmenttracker/login.html', {'form': form})


# --- DASHBOARD ---

def dashboard(request):
    """Displays Student Info and PENDING tasks only."""
    # We only want tasks where is_completed is False
    assignments = Assignment.objects.filter(is_completed=False).order_by('due_date')
    return render(request, 'assignmenttracker/dashboard.html', {
        'assignments': assignments
    })


# --- REQUIREMENTS & HISTORY ---

def add_assignment(request):
    """This is the 'Requirements' tab: Displays only DONE tasks."""
    # We only want tasks where is_completed is True
    done_tasks = Assignment.objects.filter(is_completed=True).order_by('-id')
    return render(request, 'assignmenttracker/add_assignment.html', {
        'done_tasks': done_tasks
    })


def create_task(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AssignmentForm()
    return render(request, 'assignmenttracker/create_task.html', {'form': form})

# --- TASK ACTIONS ---

def mark_done(request, task_id):
    """Moves a task from Dashboard to Requirements (History)."""
    task = get_object_or_404(Assignment, id=task_id)
    task.is_completed = True
    task.save()
    return redirect('dashboard')


def undo_task(request, task_id):
    """Moves a task from History back to the active Dashboard."""
    task = get_object_or_404(Assignment, id=task_id)
    task.is_completed = False
    task.save()
    return redirect('add_assignment')   

def add_assignment(request):
    """The Requirements tab showing both Active and Done tasks."""
    active_tasks = Assignment.objects.filter(is_completed=False).order_by('due_date')
    done_tasks = Assignment.objects.filter(is_completed=True).order_by('-id')
    
    return render(request, 'assignmenttracker/add_assignment.html', {
        'active_tasks': active_tasks,
        'done_tasks': done_tasks
    })