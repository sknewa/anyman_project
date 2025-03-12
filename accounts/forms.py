from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Post, Comment 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Use your custom User model if you have one
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'bio')  # Include the fields you want in the form

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'bio')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']  

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100)