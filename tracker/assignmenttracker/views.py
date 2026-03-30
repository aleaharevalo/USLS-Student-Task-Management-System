from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Subject, Task, Reminder
from .forms import AssignmentForm
from django.contrib.auth.models import User


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
            return render(request, 'assignmenttracker/register.html', {'error': 'Student ID already registered.'})

        try:
            user = User.objects.create_user(username=u_name, password=p_word)
            if " " in f_name:
                user.first_name, user.last_name = f_name.split(" ", 1)
            else:
                user.first_name = f_name
            user.save()
            login(request, user)
            return redirect('login')
        except Exception:
            return render(request, 'assignmenttracker/register.html', {'error': 'Registration failed.'})
            
    return render(request, 'assignmenttracker/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    pending = Task.objects.filter(user=request.user, is_done=False).order_by('due_date')
    user_subjects = Subject.objects.filter(user=request.user)

    all_tasks = Task.objects.filter(user=request.user)
    total_count = all_tasks.count()
    completed_count = all_tasks.filter(is_done=True).count()
    
    progress_percentage = 0
    if total_count > 0:
        progress_percentage = (completed_count / total_count) * 100

    subjects_with_info = []
    for sub in user_subjects:
        sub_tasks = Task.objects.filter(subject=sub, user=request.user)
        sub_total = sub_tasks.count()
        sub_done = sub_tasks.filter(is_done=True).count()
        sub_pending = sub_tasks.filter(is_done=False)
        
        sub_progress = (sub_done / sub_total * 100) if sub_total > 0 else 100
        
        
        ai_advice = ""
        
        subjects_with_info.append({
            'info': sub,
            'progress': sub_progress,
            'ai_advice': ai_advice,
            'pending_count': sub_pending.count(),
        })

    return render(request, 'assignmenttracker/dashboard.html', {
        'assignments': pending, 
        'subjects': user_subjects,
        'subjects_with_info': subjects_with_info,
        'total_count': total_count,
        'completed_count': completed_count,
        'progress_percentage': progress_percentage,
    })

@login_required
def add_assignment(request):
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
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    active_tasks = Task.objects.filter(user=request.user, is_done=False).order_by('due_date')
    done_tasks = Task.objects.filter(user=request.user, is_done=True).order_by('-due_date')[:5]
    
    return render(request, 'assignmenttracker/add_assignment.html', {
        'active_tasks': active_tasks,
        'done_tasks': done_tasks,
        'form': form 
    })

@login_required
def mark_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = True
    task.save()
    return redirect('dashboard') 

@login_required
def undo_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = False
    task.save()
    return redirect('add_assignment')

@login_required
def subject_list(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        days = request.POST.get('days')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        existing = Subject.objects.filter(user=request.user)
        for sub in existing:
            day_overlap = any(day in sub.days for day in days)
            if day_overlap:
                
                if start < str(sub.end_time) and end > str(sub.start_time):
                    messages.error(request, f"Conflict: {sub.code} is also on {sub.days} at this time.")
                    return redirect('subject_list')

        Subject.objects.create(
            user=request.user,
            code=code,
            name=request.POST.get('name'),
            days=days,
            start_time=start,
            end_time=end,
            color=request.POST.get('color', 'bg-green-700')
        )
        messages.success(request, "Subject added!")
        return redirect('subject_list')
    
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'assignmenttracker/subjects.html', {'subjects': subjects})

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

@login_required
def update_task_note(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.notes = request.POST.get('notes')
        task.save()
    return redirect('dashboard')

@login_required
def calendar_view(request):
    tasks = Task.objects.filter(user=request.user)
    reminders = Reminder.objects.filter(user=request.user)
    
    events = []

    for task in tasks:
        events.append({
            'title': f"Task: {task.title}",
            'start': task.due_date.strftime("%Y-%m-%d"),
            'color': '#006837', # Dark Green
            'url': f'/add/', # Link back to task page
        })
        
    for rem in reminders:
        events.append({
            'title': rem.title,
            'start': rem.date.strftime("%Y-%m-%d"),
            'color': '#3b82f6', # Blue
        })

    return render(request, 'assignmenttracker/calendar.html', {
        'events': events
    })

