from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Activity, Itinerary, PreferencesFormResponse
from .forms import PreferencesForm, UserRegistrationForm
from utils import helpers


def index(request):
    """
    The controller

    Args:
        request (WSGIRequest):

    Returns:
        if user is logged in and requested for an itinerary. this endpoint will return a page with the trip plan
    """
    context = {}
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        
        if form.is_valid():
            # Extract cleaned data itinerary data
            destination = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            travelers = form.cleaned_data['travelers']

            success, recommended_places_or_message = helpers.get_recommendation(destination, start_date, end_date)

            if not success:
                # In case of failure, recommended_places_or_message contains the error message.
                context['error'] = recommended_places_or_message
            else:
                # Check if user is authenticated
                if request.user.is_authenticated:
                    user = request.user
                else:
                    user = None
                itinerary_id = helpers.save_itinerary(user, destination, start_date, end_date, travelers,
                                                      recommended_places_or_message)
                # If successful, pass the structured itinerary to the context
                context['itinerary'] = recommended_places_or_message
                context['start_date'] = start_date
                context['end_date'] = end_date
                context['destination'] = destination

                return redirect(reverse('itinerary', args=[itinerary_id]))
    else:
        form = PreferencesForm()
    return render(request, 'index.html', {'form': form})

def itinerary(request, itinerary_id):
    """
    Args:
        request (WSGIRequest):
        itinerary_id (int): The ID of the itinerary.

    Returns:
        if user is logged in and requested for an itinerary. this endpoint will return a page with the trip plan
    """
    itinerary = Itinerary.objects.get(id=itinerary_id)
    days = itinerary.days.all()
    activities = Activity.objects.filter(day__in=days)
    # TODO: Only show the itinerary if the user is the owner of the itinerary, otherwise redirect to the home page.
    return render(request, 'itinerary.html', {'itinerary': itinerary, 'activities': activities})


def trips(request):
    """
    Args:
        request (WSGIRequest)
    
    Returns:
        if user is logged in, this endpoint will return a page with the user's trips
    """

    if request.user.is_authenticated:
        user = request.user
        itineraries = Itinerary.objects.filter(user=user).order_by('-start_date')
        if itineraries:
            activities = []
            for itinerary in itineraries:
                first_day = itinerary.days.first()
                first_activity = first_day.activity_set.first()
                activities.append(first_activity)
            return render(request, 'trips.html', {'itineraries': zip(itineraries, activities)})
        else:
            return render(request, 'trips.html', {'itineraries': itineraries})
    else:
        return redirect('home')


def hello_world(request):
    # Enter a name to replace "Hello World!" with "Hello {{NAME}}"
    try:
        form_data = PreferencesFormResponse.objects.latest('id')
    except:
        form_data = None
    return render(request, 'test/helloworld.html', {'name': '', 'form_data': form_data})


@login_required(login_url='admin/')
def authorized(request):
    return render(request, 'auth/authorized.html')


def signup(request):
    """
    Registers a new user and redirects to the home page.
    When a new user submits registration information, it's saved to the database, and then the user is redirected to the home page.

    Args:
        request (WSGIRequest request): request with fields to sign up/ register a user

    Returns:
        home page with the context that the user is logged in
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'home', {'form': form})


def login_view(request):
    """
    Logs in a user and redirects to the home page.
    When a user submits login credentials, it checks if the provided username and password are valid. If they are, the user is logged in and redirected to the home page.

    Args:
        request (WSGIRequest): request to log out

    Returns:
        home page
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')
    return render(request, 'home.html')


def logout_view(request):
    """
    Logs User Out

    Args:
        request (POST request): request to log out

    Returns:
        home page
    """
    logout(request)
    return redirect('home')


# Definition for the experiemental map embed page.
def map(request):
    return render(request, 'test/map.html')

def profile_view(request):
    return redirect(request, 'profile')