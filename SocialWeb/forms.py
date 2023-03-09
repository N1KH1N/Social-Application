from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from api.models import Post,ProfileAdd,Comments



class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields={"first_name","last_name","email","username","password1","password2"}
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),
        }



class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=ProfileAdd
        fields={"profile_pic","bio","user","time_line_pic"}



class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title","description","image"]

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["comment"]