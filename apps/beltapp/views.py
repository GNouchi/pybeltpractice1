from django.shortcuts import render , redirect
from django.contrib import messages
from .models import *

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def register(request):
    if request.method != 'POST':
        return redirect('/')
    result = User.objects.regValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result['user_id']
    return redirect('/wall')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    result = User.objects.loginValidator(request.POST)
    try:
        request.session['user_id'] = result['user_id']
        return redirect('/wall')
    except:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/')


def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user= User.objects.get(id = request.session['user_id'])
    my_trips = Trip.objects.all().filter(attendees = current_user)
    other_trips = Trip.objects.all().exclude(attendees = current_user)
    context = {
        'current_user' : current_user,
        'my_trips' : my_trips,
        'other_trips' : other_trips,
    }
    return render(request, 'wall.html', context)


def addtrip(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'addtrip.html')

def create(request):
    if 'user_id' not in request.session: return redirect('/')
    for x in request.POST: print(x, " : " , request.POST[x])
    result = Trip.objects.tripValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/addtrip')
    current_user = User.objects.get(id = request.session['user_id'])
    this_trip = result['newTrip']
    this_trip.attendees.add(current_user)
    messages.error(request, ("successfully created Trip to " + this_trip.destination))
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')

def destroy(request, id ):
    if 'user_id' not in request.session: 
        return redirect('/')
    this_trip = Trip.objects.get(id = id)
    if this_trip.owner.id == request.session['user_id']:
        this_trip.delete()
    return redirect('/wall')

def show(request, id ):
    if 'user_id' not in request.session: 
        return redirect('/')
    this_trip = Trip.objects.get(id = id)
    context = {
        'this_trip': this_trip,
    }
    return render(request, 'show.html', context)

def cancel(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    current_user = User.objects.get(id = request.session['user_id'])
    this_trip = Trip.objects.get(id = id)
    this_trip.attendees.remove(current_user)
    messages.error(request, ("successfully left trip " + this_trip.destination))
    return redirect('/wall')

def join(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    current_user = User.objects.get(id = request.session['user_id'])
    this_trip = Trip.objects.get(id = id)
    this_trip.attendees.add(current_user)
    messages.error(request, ("successfully joined trip to " + this_trip.destination))
    return redirect('/wall')

    # user1@user1.user1