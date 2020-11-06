from django.shortcuts import render,redirect

from  .form import  LoginForm ,SignUpForm

from  django.contrib.auth.models import  User
from  django.contrib.auth import  authenticate,login

# Create your views here.

# methode connexion
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user= authenticate(username=username,password=password)
        if user is not None:
             login(request,user)
             return  redirect("/produit")
    return render(request, "utilisateurs/login.html", {"form":form})

# methode creation utilisateur
def register_user(request):
    if request.method=="POST":
        form =SignUpForm(request.POST)
        if  form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            #email = form.cleaned_data.get("email")
            return  redirect('login')
    else:
        form = SignUpForm()
    return render(request, "utilisateurs/register.html", {"form": form})
