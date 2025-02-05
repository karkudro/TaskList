from django.shortcuts import render, redirect
from . models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password or not password2:
            messages.error(request, 'Все поля обязательны для заполнения.')
            return redirect('register')
        
        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('register')
        
        if len(password) < 8:
            messages.error(request, 'Пароль должен быть не менее 8 символов.')
            return redirect('register')
        
        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        messages.success(request, 'Вы успешно зарегистрировались.')
        return redirect('login')
    
    else:
        return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Заполните все поля.')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Неверное имя пользователя или пароль.')
            return redirect('login')
        else:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('profile')
    else:
        return render(request, 'accounts/login.html')


@login_required(login_url='login')
def profile_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(user=request.user, title=title, description=description)

    tasks = Task.objects.filter(user=request.user)

    if not tasks.exists():
        no_tasks_message = "У вас нет задач."  
    else:
        no_tasks_message = None

    return render(request, 'accounts/profile.html', {'tasks': tasks, 'no_tasks_message': no_tasks_message})


    

@login_required(login_url='login')
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'tasks': tasks})


@login_required(login_url='login')
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    
    tasks = Task.objects.filter(user=request.user)
   
    if not tasks.exists():
        return redirect('profile') 
    
    return render(request, 'accounts/profile.html', {'tasks': tasks})

