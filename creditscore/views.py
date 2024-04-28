from django.shortcuts import render,redirect
from .forms import CreditCardDataForm,CreditApplicationForm,UserProfileForm,ProfileImageForm
from .machinlearning import predict_credit_score;
import pandas as pd
from django.contrib.auth import authenticate,login,logout
from .models import User,CreditScoreResult,UserProfile
from django.contrib import messages
from.machinelearning2 import predict_user_credit_score

from .forms import ExtendedUserCreationForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='loginpage')
def creditscore(request):
    if request.method == 'POST':
        form = CreditCardDataForm(request.POST)
        if form.is_valid():
            # Assign form values to user_df
            user_df = {}
            for field in form.fields:
                user_df[field] = form.cleaned_data.get(field)

            # Convert user_df to a DataFrame
            user_df = pd.DataFrame([user_df])

            # Predict the credit score using the ScoreCard model
            credit_score_result = predict_credit_score(user_df, 'CreditScore_save5_ScoreCard.pkl')

            # Extract the credit score value as a single number from the 'CreditScore' column
            credit_score = credit_score_result['CreditScore'].iloc[0]
            credit_score=round(credit_score)

            # Pass the cleaned, single credit score value to the context
            context = {
                'form': form,
                'credit_score': credit_score  # Now just a number, not a Series or DataFrame
            }
            return render(request, 'creditscore/result.html', context)
        else:
            # If the form is not valid, pass form errors
            context = {'form': form}
            return render(request, 'creditscore/result.html', context)
    else:
        # For GET requests, just show the initial form
        form = CreditCardDataForm()
        context = {'form': form}
        return render(request, 'creditscore/Scoreboard.html', context)


def landingpage(request):
    return render(request,'creditscore/LandingPage.html')


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, "creditscore/loginpage.html")  

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password")

    return render(request, "creditscore/loginpage.html")


def credit_score_view(request):
    if request.method == 'POST':
        form = CreditApplicationForm(request.POST)
        if form.is_valid():
            # Extracting the data from the form
            type_of_loan = form.cleaned_data['type_of_loan']
            payment_behaviour = form.cleaned_data['payment_behaviour']
            total_emi_per_month = form.cleaned_data['total_emi_per_month']
            monthly_inhand_salary = form.cleaned_data['monthly_inhand_salary']
            num_bank_accounts = form.cleaned_data['num_bank_accounts']
            num_credit_cards = form.cleaned_data['num_credit_cards']
            interest_rate = form.cleaned_data['interest_rate']
            num_of_loan = form.cleaned_data['num_of_loan']
            delay_from_due_date = form.cleaned_data['delay_from_due_date']
            num_of_delayed_payment = form.cleaned_data['num_of_delayed_payment']
            changed_credit_limit = form.cleaned_data['changed_credit_limit']
            num_credit_inquiries = form.cleaned_data['num_credit_inquiries']
            credit_mix = form.cleaned_data['credit_mix']
            outstanding_debt = form.cleaned_data['outstanding_debt']
            credit_utilization_ratio = form.cleaned_data['credit_utilization_ratio']
            credit_history_age = form.cleaned_data['credit_history_age']
            payment_of_min_amount = form.cleaned_data['payment_of_min_amount']
            amount_invested_monthly = form.cleaned_data['amount_invested_monthly']

            credit_score = predict_user_credit_score(
                type_of_loan, payment_behaviour, total_emi_per_month, monthly_inhand_salary,
                num_bank_accounts, num_credit_cards, interest_rate, num_of_loan, delay_from_due_date,
                num_of_delayed_payment, changed_credit_limit, num_credit_inquiries, credit_mix,
                outstanding_debt, credit_utilization_ratio, credit_history_age, payment_of_min_amount,
                amount_invested_monthly
            )

            # Pass the credit score to the template or return it in the response
            return render(request, 'creditscore/result2.html', {'credit_score': credit_score})
    else:
        form = CreditApplicationForm()

    return render(request, 'creditscore/Test101.html', {'form': form})


def RegisterPage(request):
    form = ExtendedUserCreationForm()
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user object to the database
            UserProfile.objects.create(  # Create the user profile with default values
                user=user,
                bank_balance=0,  
                current_bank="",  
                phone_number="",  
                # The profile image will have the default set in the model
            )
            login(request, user)  # Log in the user
            return redirect('home')

    context = {'form': form}
    return render(request, 'creditscore/signUp.html', context)

def creditpay(request):
    return render(request,'creditscore/creditpayback.html')


@login_required(login_url='loginpage')
def save_credit_score(request):
    if request.method == 'POST':
        credit_score = request.POST.get('credit_score')

        # Debug: Check if credit_score is received
        if not credit_score:
            messages.error(request, "No credit score received.")
            return render(request, 'creditscore/result.html')

        try:
            # Try converting the credit score to an integer
            credit_score = int(credit_score)
            # Create a new record in the database
            CreditScoreResult.objects.create(user=request.user, Score=credit_score)
            messages.success(request, 'Your credit score has been successfully saved!')
            return redirect('home')  
        except ValueError:
            # If there's an error in converting the credit score to an integer
            messages.error(request, "Invalid credit score provided.")
            return render(request, 'creditscore/result.html')

    # If it's not a POST request, or other issues
    return render(request, 'creditscore/result.html')


def aboutpage(request):
    return render(request,'creditscore/AboutPage.html')

def contactpage(request):
    return render(request,'creditscore/ContactPage.html')

@login_required(login_url='loginpage')
def homepage(request):
    return render(request,'creditscore/homePage.html')


def logoutuser(request):
    logout(request)
    return redirect('landingpage')

def viewprofile(request):
    user = request.user  # Get the current logged-in user
    user_profile = user.profile  # Access the related UserProfile

    context = {
        'user': user,
        'user_profile': user_profile,
    }
    
    return render(request,'creditscore/userProfile.html',context)


@login_required(login_url='loginpage')
def editprofile(request):
    user = request.user
    profile = user.profile  # Assumes a OneToOne relation exists

    if request.method == 'POST':
        user_form = ExtendedUserCreationForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        # Extracting the data for the user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        # Checking if the data for the user is valid
        if user_form.is_valid():
            user.save()
            messages.success(request, 'User information updated successfully!')
        
        # Checking if the profile form is valid
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            
        return redirect('view-profile')  # Redirect to the profile view after updating

    else:
        user_form = ExtendedUserCreationForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'creditscore/editProfile.html', context)


@login_required(login_url='loginpage')
def editprofileimage(request):
    user = request.user
    profile = user.profile  
    
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile image updated successfully!')
            return redirect('view-profile')  
    else:
        form = ProfileImageForm(instance=profile)

    context = {'form': form, 'profile': profile}
    return render(request, 'creditscore/editPhoto.html', context)


def credhist(request):
    credit_score_results = CreditScoreResult.objects.filter(user=request.user).order_by('created')

    dates = [result.created.strftime('%Y-%m-%d') for result in credit_score_results]
    scores = [result.Score for result in credit_score_results]

    # Pass the data to the template
    context = {
        'dates': dates,
        'scores': scores,
    }
    return render(request, 'creditscore/credHistory.html', context)