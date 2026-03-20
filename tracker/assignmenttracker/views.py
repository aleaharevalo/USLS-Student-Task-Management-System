from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Subject, Task
from .forms import AssignmentForm
from django.contrib.auth.models import User

# --- AUTHENTICATION ---

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'assignmenttracker/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        f_name = request.POST.get('full_name')
        p_word = request.POST.get('password')

        # Check if user already exists
        if User.objects.filter(username=u_name).exists():
            return render(request, 'assignmenttracker/register.html', {'error': 'Student ID already registered.'})

        try:
            # Create user
            user = User.objects.create_user(username=u_name, password=p_word)
            
            # Optional: Store full name
            if " " in f_name:
                user.first_name, user.last_name = f_name.split(" ", 1)
            else:
                user.first_name = f_name
            user.save()

            login(request, user)
            return redirect('dashboard')
        except Exception as e:
            return render(request, 'assignmenttracker/register.html', {'error': 'Registration failed. Please try again.'})
            
    return render(request, 'assignmenttracker/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- DASHBOARD & TASKS ---

@login_required
def dashboard(request):
    # Fetch the data
    pending = Task.objects.filter(user=request.user, is_done=False).order_by('due_date')
    user_subjects = Subject.objects.filter(user=request.user)
    
    return render(request, 'assignmenttracker/dashboard.html', {
        'assignments': pending, 
        'subjects': user_subjects,
    })

@login_required
def add_assignment(request):
    """This is now your UNIFIED page: Form + List"""
    
    # 1. Handle Form Submission (The logic from create_task)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added to ledger.")
            return redirect('add_assignment')
    else:
        form = AssignmentForm()
        # Ensure the dropdown only shows the user's subjects
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    # 2. Fetch Data for the Ledger
    active_tasks = Task.objects.filter(user=request.user, is_done=False).order_by('due_date')
    done_tasks = Task.objects.filter(user=request.user, is_done=True).order_by('-due_date')[:5]
    
    return render(request, 'assignmenttracker/add_assignment.html', {
        'active_tasks': active_tasks,
        'done_tasks': done_tasks,
        'form': form  # Pass the form to the template
    })


# Matches path('mark-done/<int:task_id>/', views.mark_done...)
@login_required
def mark_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = True
    task.save()
    return redirect('add_assignment')

# Matches path('undo/<int:task_id>/', views.undo_task...)
@login_required
def undo_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = False
    task.save()
    return redirect('add_assignment')

# --- SUBJECTS ---

# Matches path('subjects/', views.subject_list...)
@login_required
def subject_list(request):
    if request.method == 'POST':
        Subject.objects.create(
            user=request.user,
            code=request.POST.get('code'),
            name=request.POST.get('name'),
            days=request.POST.get('days'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            color=request.POST.get('color', 'bg-green-700')
        )
        messages.success(request, "Subject added!")
        return redirect('subject_list')
    
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'assignmenttracker/subjects.html', {'subjects': subjects})

# Matches path('subjects/drop/<int:subject_id>/', views.drop_subject...)
@login_required
def drop_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.delete()
    messages.info(request, "Subject dropped.")
    return redirect('subject_list')

@login_required
def schedule_view(request):
    user_subjects = Subject.objects.filter(user=request.user)
    
    context = {
        'subjects': user_subjects,
        'hours': ["07", "08", "09", "10", "11", "12", "01", "02", "03", "04", "05"],
        'days': ["MON", "TUE", "WED", "THU", "FRI"]
    }
    
    return render(request, 'assignmenttracker/schedule.html', context)