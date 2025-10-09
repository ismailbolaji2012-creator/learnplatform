
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Module

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title','description','price']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title','description','order','video_url','note']
