from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import models
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import requests
from .forms import TaskForm
# Create your views here.
# ADMIN= blessing
# PASSWORD = blessing

@login_required
def index(request):
    if request.method == 'POST':
        task = request.POST['addTask']
        
        if models.Todo.objects.filter(user=request.user, todo_name =task).exists():
            messages.error(request, f"{task} already added")
            return redirect(index)
        else:
            new_task = models.Todo(user=request.user, todo_name = task)
            new_task.save()
        
    
            
    
    get_task = models.Todo.objects.filter(user=request.user).order_by('-date')
    task_count = models.Todo.objects.filter(user = request.user).count()
    

    
    context ={
        'get_task' : get_task,
        'task_count' : task_count,
    }
    return render(request, 'temp/index.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if models.CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if models.CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"{email} has been registered")
            return redirect('register')
        
        api_key = "bf00a69de8d34a82bac4ea98b41f29fd"
        email_validation = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}")
        
        if email_validation.status_code == 200:
            data = email_validation.json()
            if data['deliverability'] == 'UNDELIVERABLE':
                messages.error(request, f'{email} is not valid')
                return redirect('register')
        
        if len(password) < 4:
            messages.error(request, 'Password must be at least 4 characters')
            return redirect('register')
        
        user = models.CustomUser.objects.create_user(username, email, password)
        # CustomUser.objects.create_user(username, email, password)
        if user:
            subject = 'TODO APP - REGISTRATION SUCCESSFUL!'
            message = f"Hi {username},\n\n You've successfully registered for TODO APP.\n Thank you!\n\n\nRegards;\nTODO Team\n\n\n Note: This is a system generated message, please do not reply."
            sender = 'adeblessinme4u@gmail.com'  
            receiver = [email]
        
            send_mail(subject, message, sender, receiver, fail_silently=True)
            # send_mail(subject, message, sender, receiver)
            # send_mail.fail_silently = True
        else:
            subject = 'TODO APP - REGISTRATION SUCCESSFUL!'
            message = f"Hi {username},\n\n There's an error while creating your account, \nplease try again or contact the admin.\n Thank you!\n\n\nRegards;\nTODO Team\n\n\n Note: This is a system generated message, please do not reply."
            sender = 'adeblessinme4u@gmail.com'  
            receiver = [email]
        
            send_mail(subject, message, sender, receiver)
            send_mail.fail_silently = True
        
        messages.success(request, 'Account created successful')
        return redirect('login')
    
    return render(request, 'temp/sign-up.html')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
        
       
         
#         username_comfirmation = User.objects.filter(username=username)
#         # email_confirmation = User.objects.filter(email= email)
#         if username_comfirmation:
#             messages.error(request, 'Username already exits')
#             return redirect(register)
        
#         if User.objects.filter(email =email):
#             messages.error(request, f"{email} has been registered")
#             return redirect(register)
        
    
#         api_key = "bf00a69de8d34a82bac4ea98b41f29fd"
#         email_validation = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}")
        
#         if email_validation.status_code ==200:
#             data = email_validation.json()
#             if data['deliverability'] == 'UNDELIVERABLE':
#                 messages.error(request,f'{email} is not valid')
#                 return redirect(register)
#             else:
#                 pass
                    
        
#         if len(password) < 4:
#             messages.error(request, 'Password must be at least 4 characters')
#             return redirect('register')
       
       
          
#         user = User.objects.create_user(username,email,password)
#         user.save()
        
#         if user:
#             subject = 'TODO APP - REGISTRATION SUCCESSFUL!'
#             message = f"Hi {username},\n\n You've successfully registered for TODO APP.\n Thank you!\n\n\nRegards;\nTODO Team\n\n\n Note: This is a system generated message, please do not reply."
#             sender = 'adeblessinme4u@gmail.com'  
#             receiver = [email]
        
#             send_mail(subject, message,sender,receiver)
#             send_mail.fail_silently = True
            
#         else:
#             subject = 'TODO APP - REGISTRATION SUCCESSFUL!'
#             message = f"Hi {username},\n\n There's an error while creating your account, \nplease try again or contact the admin.\n Thank you!\n\n\nRegards;\nTODO Team\n\n\n Note: This is a system generated message, please do not reply."
#             sender = 'adeblessinme4u@gmail.com'  
#             receiver = [email]
        
#             send_mail(subject, message,sender,receiver)
#             send_mail.fail_silently = True
        
#         messages.success(request, 'Accout created succesful')
#         return redirect('login')
    
#     return render(request, 'temp/sign-up.html')


def Logout(request):
    logout(request)
    return redirect('login')

# def Login(request):
#     if request.method == 'POST':
#         username = request.POST.get('name') 
#         password = request.POST.get('password') 
        
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             messages.error(request, 'Error, User not found :)')
#             return redirect('login')
#     return render(request, 'temp/signin.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        
        # TO CHECK IF USER EXIST IN DATABASE
        validate_user = authenticate(request, username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('index')
        
        else: 
            messages.error(request, 'Error, User not found :)')
            return redirect('login')
    return render(request, 'temp/signin.html')

@login_required
def DeleteTask(request, name):
    get_task = models.Todo.objects.get(user=request.user, todo_name = name)
    get_task.delete()
    return redirect('index')
 


@login_required
def EditTask(request, pk):
    get_task = models.Todo.objects.get(user=request.user, id = pk)
    form = TaskForm(instance=get_task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance= get_task)
        if form   == '':
            messages.error(request, "The Field below is required ") 
        elif form.is_valid():
            form.save()
            return redirect('index')
        
        else:
            form = TaskForm(instance=get_task)
    context = {
        "form": form,
    }
   
    return render(request, 'temp/edit.html', context)
    