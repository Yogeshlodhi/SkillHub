from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room,Topic,Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {'id': 1, 'name': 'Yogesh Kumar'},
#     {'id': 2, 'name': 'Geeta Lodhi'},
#     {'id': 3, 'name': 'Sagar Das'},
# ]


def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}    

    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    # page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html',{'form': form})

def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.all()

    # rooms = Room.objects.filter(topic__name__icontains=q) # contains is CASE SENSITIVE ----------> icontains ===> NOT CASE SENSITIVE
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) # contains is CASE SENSITIVE ----------> icontains ===> NOT CASE SENSITIVE
    # rooms = Room.objects.filter(topic__name=q)
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    # room_messages = Message.objects.all()

    context = {'rooms' : rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)
    # return render(request, 'home.html', {'rooms': rooms})
    # return HttpResponse('Home Page')


def Rooms(request,pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    # context  = {'room': room}
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') # many to one
    participants = room.participants.all() # many to many

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('rooms',pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages,'participants':participants,}
    return render(request, 'base/room.html', context)
    # return HttpResponse('Rooms Only')

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # we can get all the children of a specific object by doing the modelname_set.all()
    room_messages =  user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics,}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     # form.save()
        #     room.save()
        return redirect('home') 

    context = {'form' : form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to update')

    if request.method == 'POST':
        form = RoomForm(request.POST,request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
     
    context = {'form': form, 'topics': topics, } 
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    # rooms = Room.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to update')

    if request.method == 'POST':
        # rooms = rooms.filter(room)
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    # rooms = Room.objects.all()

    if request.user != message.user:
        return HttpResponse('You are not allowed to update')

    if request.method == 'POST':
        # rooms = rooms.filter(room)
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)

    return render(request,'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html',{'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})