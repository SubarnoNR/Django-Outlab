from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import requests


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150,required=True)
    email = forms.EmailField(max_length=200,required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name' ,'password1', 'password2', )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user_info = requests.get('https://api.github.com/users/{}'.format(username))
        if user_info.status_code == 404:
            raise forms.ValidationError("No such GitHub user exists. Please check username!")
        return username
    
    def save(self, commit = True):
        user = super(SignUpForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        
        return user