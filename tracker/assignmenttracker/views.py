from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Assignment, Subject
from .forms import AssignmentForm

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
        
        if User.objects.filter(username=u_name).exists():
            return render(request, 'assignmenttracker/register.html', {'error': 'Student ID already registered!'})

        # Create user and split name for the Dashboard Student Info
        user = User.objects.create_user(username=u_name, password=p_word)
        if " " in f_name:
            user.first_name, user.last_name = f_name.split(" ", 1)
        else:
            user.first_name = f_name
        user.save()
        return redirect('login')
    return render(request, 'assignmenttracker/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# --- DASHBOARD & REQUIREMENTS ---

@login_required
def dashboard(request):
    # assignments.filter(user=request.user) ensures isolation
    assignments = Assignment.objects.filter(user=request.user, is_completed=False).order_by('due_date')
    return render(request, 'assignmenttracker/dashboard.html', {'assignments': assignments})

@login_required
def add_assignment(request):
    active_tasks = Assignment.objects.filter(user=request.user, is_completed=False).order_by('due_date')
    done_tasks = Assignment.objects.filter(user=request.user, is_completed=True).order_by('-id')
    return render(request, 'assignmenttracker/add_assignment.html', {
        'active_tasks': active_tasks, 
        'done_tasks': done_tasks
    })


# --- TASK ACTIONS ---

@login_required
def create_task(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Attach the student
            task.save()
            return redirect('dashboard')
    else:
        form = AssignmentForm()
        # This is the important part!
        # It filters the dropdown to ONLY show the user's subjects
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
        if 'subject' in form.fields:
            form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
        
    return render(request, 'assignmenttracker/create_task.html', {'form': form})

@login_required
def mark_done(request, task_id):
    # get_object_or_404(..., user=request.user) prevents people from marking others' tasks as done
    task = get_object_or_404(Assignment, id=task_id, user=request.user)
    task.is_completed = True
    task.save()
    return redirect('add_assignment')

@login_required
def undo_task(request, task_id):
    task = get_object_or_404(Assignment, id=task_id, user=request.user)
    task.is_completed = False
    task.save()
    return redirect('add_assignment')

@login_required
def subject_list(request):
    if request.method == "POST":
        name = request.POST.get('name')
        code = request.POST.get('code')
        days = request.POST.get('days')
        time = request.POST.get('time')
        
        Subject.objects.create(
            user=request.user,
            name=name,
            code=code,
            days=days,
            time=time
        )
        return redirect('subject_list')

    # Only show subjects belonging to this user
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'assignmenttracker/subjects.html', {'subjects': subjects})