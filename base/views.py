from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from django.http import HttpResponse

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me!'},
#     {'id': 3, 'name': 'Frontend Developers!'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = user.objects.get(username=username)
        except:
            #messages.error(request, 'User does not exist')
            pass
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User or password does not match')
            
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')    

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')
        
    #context = {'page':page}
    return render(request, 'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    # return HttpResponse('Home Page')
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms':rooms,'topics':topics, "room_count":room_count} 
    return render(request, 'base/home.html', context)



def room(request,pk):
    #room = None
    
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room = i
    
    room = Room.objects.get(id=pk)
    context = {'room': room}
    # return HttpResponse('Room')
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method=="POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/room_form.html', context)
    

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    #Pre-filling of the information
    form = RoomForm(instance=room) 
    
    if request.user != room.host :
        return HttpResponse('You are not allowed here.')
    
    if request.method=="POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(pk=pk)
    #Pre-filling of the information
    form = RoomForm(instance=room) 
    
    if request.user != room.host :
        return HttpResponse('You are not allowed here.')
    
    if request.method=="POST":
        room.delete() 
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':room})
    