from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from itineraries.forms import userRegistrationForm
from django.contrib import messages  # Import messages framework

from utils import helpers

# Create your views here.
def index(request):
    return render(request, 'index.html')


def destination_search(request):
    context = {}
    if request.method == 'POST':
        destination = request.POST.get('destination')
        success, recommended_places_or_message = helpers.get_recommendation(destination)

        if not success:
            # In case of failure, recommended_places_or_message contains the error message.
            context['error'] = recommended_places_or_message
        else:
            # On success, it contains the list of places (which may be empty).
            context['places'] = recommended_places_or_message

    return render(request, 'test/destinations.html', context)



    # return render(request, 'test/destinations.html', {'name': ''})

@login_required(login_url='admin/')
def authorized(request):
    return render(request, 'auth/authorized.html')

def register(request):
    if request.method == 'POST':
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../hello')
    else:
        form = userRegistrationForm()
    return render(request, 'auth/signup.html', {'form': form})

#Definition for the experiemental map embed page.
def map(request):
    return render(request, 'test/map.html')