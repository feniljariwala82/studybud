from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import RoomCreateForm
from .models import Room
from .models import Topic


# Create your views here.
def home(request):
    query = request.GET.get('topic') if request.GET.get('topic') != None else ''

    print(query)
    # here, double underscore means, we preload name of topic object,
    # like preload(topic).name -> adonisjs reference
    # icontains means it will apply the query without being concerned about the case
    rooms = None
    try:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query))
    except ObjectDoesNotExist:
        print('We did not find anything')

    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': rooms.count()}
    return render(request, 'base/home.html', context)


@login_required(login_url='auth.login')
def rooms_show(request, pk):
    selected_room = Room.objects.get(id=pk)
    context = {'selected_room': selected_room}
    return render(request, 'base/rooms/show.html', context)


@login_required(login_url='auth.login')
def rooms_create(request):
    form = RoomCreateForm()
    context = {'form': form}
    return render(request, 'base/rooms/create.html', context)


@login_required(login_url='auth.login')
def rooms_store(request):
    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.index')
        else:
            print('Invalid form data')
            return redirect('rooms.create')
    else:
        print('Invalid http request')
        return redirect('rooms.create')


@login_required(login_url='auth.login')
def rooms_edit(request, pk):
    room = Room.objects.get(id=pk)

    # validating user
    if request.user != room.host:
        messages.error(request, 'You are not allowed to perform this operation')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # by doing this we tell python to prefill the form data
    form = RoomCreateForm(instance=room)
    context = {'form': form, 'room_id': room.id}
    return render(request, 'base/rooms/edit.html', context)


@login_required(login_url='auth.login')
def rooms_update(request, pk):
    if request.method == 'POST':
        room = Room.objects.get(id=pk)

        # validating user
        if request.user != room.host:
            messages.error(request, 'You are not allowed to perform this operation')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # here instance? by doing this we told python to update this particular record
        form = RoomCreateForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home.index')
        else:
            print('Invalid form data')
            return redirect('home.index')
    else:
        print('Invalid http request')
        return redirect('home.index')


@login_required(login_url='auth.login')
def rooms_delete(request, pk):
    room = Room.objects.get(id=pk)

    # validating user
    if request.user != room.host:
        messages.error(request, 'You are not allowed to perform this operation')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # post method
    if request.method == 'POST':
        room.delete()
        return redirect('home.index')
    else:
        # get method
        context = {'id': pk, 'item_name': room.name, 'item_type': 'room'}
        return render(request, 'components/delete.html', context)
