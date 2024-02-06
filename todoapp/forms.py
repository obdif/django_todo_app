from django import forms
# from django.contrib.auth.models import User
from .models import Todo

# class RegisterForm(forms.Form):
#     userName = forms.CharField(max_length= 3)
#     email = forms.EmailField( required=True)
#     password = forms.CharField(widget=forms.PasswordInput)
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo_name']