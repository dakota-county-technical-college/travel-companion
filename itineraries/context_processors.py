from .forms import UserRegistrationForm, UserLoginForm

def login_form(request):
    return {'login_form': UserLoginForm()}

def register_form(request):
    return {'register_form': UserRegistrationForm()}