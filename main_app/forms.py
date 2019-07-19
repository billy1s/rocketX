from django import forms
from django.contrib.auth.models import User
from main_app.models import userProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')





class searchForm(forms.Form):
    date_start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date Start'
    )
    date_end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date end'
    )