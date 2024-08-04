from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, User, Message
from .forms import RoomForm

# Create your views here.

def loginPage(req):
    page = 'login'
    if req.user.is_authenticated:
        return redirect('home')
    
    if req.method == 'POST':
        username = req.POST.get('username').lower()
        password = req.POST.get('password')
        try:
            user = User.objects.get(username= username)
        except:
            messages.error(req, 'User Doesnot Exist')
        user = authenticate(req, username=username, password=password)
        if user  is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, 'Username/Password Doesnot Exist')

    context={'page':page}
    return render(req, 'base/login_page.html', context)

def registerUser(req):
    page = 'register'
    form = UserCreationForm()

    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(req, user)
            return redirect('home')
        else:
            print('Form is not valid')
            messages.error(req, 'Error Occured during Reg')

    context = {'form': form, 'page': page}
    return render(req, 'base/login_page.html', context)

def logoutUser(req):
    logout(req)
    return redirect('home')

def home(req):
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) | 
        Q(desc__icontains=q)
        )
    
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(req, 'base/home.html', context)

def room(req, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') # type: ignore
    participants = room.participants.all()
    if req.method == 'POST':
        message = Message.objects.create(
            user=req.user, 
            room=room, 
            body=req.POST.get('body')
        )
        room.participants.add(req.user)
        return redirect('room', pk= room.id) # type: ignore

    context = {'room': room, 'room_messages' : room_messages, 'participants': participants}
    return render(req, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() #type:ignore
    topics = Topic.objects.all()
    room_messages = user.message_set.all() #type:ignore
    context = {'user': user, 'rooms': rooms, 
               'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/profile.html', context)

@login_required(login_url="/login")
def create_room(req):
    if req.user.username == 'admin':
        form = RoomForm()
        if req.method == 'POST':
            form = RoomForm(req.POST)
            if form.is_valid():
                form.save()
                return redirect('home')

        context = {'form': form}
        return render(req, 'base/room_form.html', context)
    else:
        return render(req, 'home')

@login_required(login_url="/login")
def updateRoom(req, pk):
    if req.user.username == 'admin':
        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)

        if req.method == 'POST':
            form = RoomForm(req.POST, instance=room)
            if form.is_valid():
                form.save()
                return redirect('home')
        
        context = {'form':form}
        return render(req, 'base/room_form.html', context)
    else:
        return render(req, 'home')
    

@login_required(login_url="/login")
def deleteRoom(req, pk):
    if req.user.username == 'admin':
        room = Room.objects.get(id=pk)
        if req.method == 'POST':
            room.delete()
            return redirect('home')
        return render(req, 'base/delete.html', {'obj': room})
    else:
        return render(req, 'home')

@login_required(login_url="/login") 
def deleteComment(req, pk):
    
    message = Message.objects.get(id=pk)
    if req.user != message.user and req.user.username != 'admin':
        return HttpResponse('You are Not allowed to do this operation')
    if req.method == 'POST':
        message.delete()
        return redirect('home')
    return render(req, 'base/delete.html', {'obj': message})
