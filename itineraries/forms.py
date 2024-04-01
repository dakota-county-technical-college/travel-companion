from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['id'] = 'login_' + field_name
            field.widget.attrs['name'] = 'login_' + field_name

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        # `password1` and `password2` don't need to be defined again since they're already included in `fields`
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['id'] = 'register_' + field_name
            field.widget.attrs['name'] = 'register_' + field_name
    
class PreferencesForm(forms.Form):
    destination = forms.CharField(max_length=100)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'hide-datepicker'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'hide-datepicker'}))
    travelers = forms.IntegerField(min_value=1)