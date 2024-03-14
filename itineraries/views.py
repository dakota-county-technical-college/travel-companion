from django.shortcuts import render

# Create your views here.
def hello_world(request):
    # Enter a name to replace "Hello World!" with "Hello {{NAME}}"
    return render(request, 'helloworld.html', {'name': ''})