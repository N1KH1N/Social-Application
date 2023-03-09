# Create your views here.
from django.shortcuts import render,redirect
from django.views.generic import View
from SocialWeb.forms import LoginForm,RegistrationForm,UserProfileForm,PostForm,CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import Post,ProfileAdd,Comments
from django.views.generic import View,CreateView,FormView,TemplateView,ListView,UpdateView
from django.urls import reverse_lazy


class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(form.cleaned_data)
            return redirect("signin")
        else:
            return render(request,"register.html",{"form":form})

class LoginView(View):

    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form}) 

# class ProfileCreateView(View):
#     def get(self,request,*args,**kwargs):
#         form=UserProfileForm()
#         return render(request,"profile-create.html",{"form":form}) 

#     def post(self,request,*args,**kwargs):
#         form=UserProfileForm(request.POST,files=request.FILES)
#         if form.is_valid():
#             form.instance.user=request.user
#             form.save()
#             return redirect("profile")
#         else:
#             return render(request,"profile-create.html",{"form":form})




class ProfileCreateView(CreateView):
    model=ProfileAdd
    form_class=UserProfileForm
    template_name="user-profile.html"
    success_url=reverse_lazy("profile_detail")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class HomeView(CreateView,ListView):
    model=Post
    form_class=PostForm
    template_name="index.html"
    success_url=reverse_lazy("home")
    context_object_name="posts"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        return Post.objects.all().order_by("-date")
    

class UserprofileView(TemplateView):
    template_name="profile-detail.html"


class AddCommentView(View):
    def post(self,request,*args,**kwargs):
        pid=kwargs.get("id")
        pos=Post.objects.get(id=pid)
        usr=request.user
        com=request.POST.get("comment")
        Comments.objects.create(user=usr,post=pos,comment=com)
        return redirect("home")
        
    
class ProfileUpdateView(UpdateView):
    model=ProfileAdd
    form_class=UserProfileForm
    template_name="profile-change.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"


class UpvoteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pt=Post.objects.get(id=id)
        pt.upvote.add(request.user)
        pt.save()
        return redirect("home")
    
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Post.objects.get(id=id).delete()
        return redirect("home")
    
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

class UpvoteRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pt=Post.objects.get(id=id)
        pt.upvote.remove(request.user)
        pt.save()
        return redirect("home")    
    
class Commentupvoteview(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cmt=Comments.objects.get(id=id)
        cmt.upvote.add(request.user)
        cmt.save()
        return redirect("home")
    
class CommentdeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Comments.objects.get(id=id).delete()
        return redirect ("home")