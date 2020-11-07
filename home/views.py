from django.shortcuts import render,redirect
from .forms import SearchForm,NewUserCreationForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
import wikipedia
from .forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import Past_search



def login_user(request):
    if request.method=="POST":
        form=AuthenticationForm(request.POST)
        if form.is_valid():

            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"You are Logged In Successfully! as {username}")
                return HttpResponseRedirect('/home')
            else:
                messages.error(request,"Invalid Username or Password!")

            #else:messages.error(request,"Invalid Username or Password!!")


    form=AuthenticationForm()
    return render(request,'home/login.html',{'form':form})

def logout_user(request):
    logout(request)
    messages.info(request,"Logged Out Successfully")
    return HttpResponseRedirect('/home')

def signup(request):
    if request.method=="POST":
        form=NewUserCreationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            confirmpassword=form.cleaned_data['confirmpassword']
            if password!=confirmpassword:
                form=NewUserCreationForm()
                errormessage="Both Passwords Should MATCH!"
                return render(request,'home/signup.html',{'form':form,'errormessage':errormessage})


            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                return HttpResponseRedirect('/home/login')

    else:
        form=NewUserCreationForm()

    return render(request,'home/signup.html',{'form':form})

def validate_username(request):
    username=request.GET.get('username',None)
    data={
        'is_taken':User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def home(request):
    user=request.user

    if user.is_authenticated:
        user_obj=User.objects.get(username=user)
        if request.method=="GET":
            form=SearchForm()
            return render(request,'home/home.html',{'form':form,'is_authenticated':True})
        if request.method=='POST':

            form=SearchForm(request.POST)
            if form.is_valid():
                to_search = form.cleaned_data['to_search']
                past_search=Past_search.objects.create(user=user_obj,search_name=to_search)
                past_search.save()
                search = wikipedia.search(to_search)
                summary = wikipedia.summary(to_search)
                page=wikipedia.page(to_search)
                try:
                    page = wikipedia.page(to_search)
                except wikipedia.exceptions.DisambiguationError as e:
                    print (e.option)
                title = page.title
                url= page.url
                return render(request,'home/home.html',{'form':form,'search':search,'title':title,'url':url,'summary':summary,'is_authenticated':True})
                #return HttpResponse("SUCCESS")

    else:
        form=SearchForm()
    return render(request,'home/home.html',{'form':form})

def past_search(request):
    user=request.user
    user_obj=User.objects.get(username=user)
    if user.is_authenticated:
        past_searches=Past_search.objects.filter(user=user_obj)#Their is a differnce between user and user_obj
        return render(request,'home/past_search.html',{'past_searches':past_searches})


# Create your views here.
