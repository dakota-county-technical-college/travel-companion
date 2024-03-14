from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def hello_world(request):
    # Enter a name to replace "Hello World!" with "Hello {{NAME}}"
    return render(request, 'helloworld.html', {'name': ''})

@login_required(login_url='/admin/')
def authorized(request):
    return render(request, 'authorized.html')