from django.forms import ModelForm
from .models import CreditCardData,CreditApplication,UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreditCardDataForm(ModelForm):
    class Meta:
        model = CreditCardData
        fields = '__all__'
        exclude = ['label', 'user']
    
    # this will create a drop down that will allow the users to see what the numbers correspond to, ie male and not input 1 
    SEX_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    ]

    EDUCATION_CHOICES = [
        (1, 'Graduate School'),
        (2, 'University'),
        (3, 'High School'),
        (4, 'Others'),
        (5, 'Unknown'),
        (6, 'None'),
    ]

    MARRIAGE_CHOICES = [
        (1, 'Single'),
        (2, 'Married'),
        (3, 'Other'),
    ]

    SEX = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    EDUCATION = forms.ChoiceField(choices=EDUCATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    MARRIAGE = forms.ChoiceField(choices=MARRIAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class CreditApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        fields = '__all__'

# here i have to extent the user model,and create the form
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


class ProfileImageForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']