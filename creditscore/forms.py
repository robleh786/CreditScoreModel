from django.forms import ModelForm
from .models import CreditCardData,CreditApplication,UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreditCardDataForm(ModelForm):
    ID = forms.IntegerField()
    class Meta:
        model = CreditCardData
        fields = '__all__'
        exclude = ['label','user'] 

    MARRIAGE_CHOICES = [
        (1, 'Single'),
        (2, 'Married'),
        (3, 'Other'),
    ]

    MARRIAGE = forms.ChoiceField(choices=MARRIAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class CreditApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        fields = '__all__'


class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bank_balance', 'current_bank', 'phone_number', 'profile_image']