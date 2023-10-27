import re

from django import forms

from .models import Profile, User


class LoginForm(forms.Form):
    dni = forms.CharField(label="DNI", widget=forms.TextInput, max_length=9)
    password = forms.CharField(widget=forms.PasswordInput)

    def check_dni(self):
        dni_regex = "[0-9]{8}[A-Z]"
        cd = self.cleaned_data

        if re.match(dni_regex, cd['dni']) is None:
            raise forms.ValidationError('Please insert a valid DNI')
        return cd['dni']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['dni', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
