from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
# Create your views here.
from django.http import HttpResponse
from .forms import RegisterForm,PostForm
from .models import User,Post
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def RegisterUser(request):
    thank = False
    if request.method == 'POST':
        form_user = RegisterForm(request.POST)
        if form_user.is_valid():
            user = form_user.save()
            user.save()
            thank = True
            print(user)
            return redirect("/post")
    context ={}
    context['form']= RegisterForm()
    return render(request, 'register.html', context)


def index(request):
    return render(request, 'index.html')

def LoginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        print(email,password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect("/add-post")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_request(request):
    logout(request)
    messages.info(request, "you have been logged out")
    return redirect("/login")

@login_required(login_url='/login')
def addPost(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('/all-post')
    context = {}
    context['form']= PostForm()
    return render(request,'post.html',context)

@login_required(login_url='/login')
def allPost(request):
    myPosts = Post.objects.filter(user= request.user)
    return render(request,'postList.html', {'myposts': myPosts})    
