from django.shortcuts import render,redirect
from .forms import CreditCardDataForm,CreditApplicationForm,UserProfileForm,ProfileImageForm
from .machinlearning import predict_credit_score;
import pandas as pd
from django.contrib.auth import authenticate,login,logout
from .models import User,CreditScoreResult,UserProfile,LoanResult
from django.contrib import messages
from.machinelearning2 import predict_user_credit_score

from .forms import ExtendedUserCreationForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='loginpage')
def creditscore(request):
    # dfine the requet method, only post will it pass through
    if request.method == 'POST':
        form = CreditCardDataForm(request.POST)
        # this will error check the form for me 
        if form.is_valid():
            
            user_df = {}
            # pass it all through the model
            for field in form.fields:
                user_df[field] = form.cleaned_data.get(field)

            
            user_df = pd.DataFrame([user_df])

            # used my saved combiner/scocard to predict the score
            credit_score_result = predict_credit_score(user_df, 'CreditScore_save5_ScoreCard.pkl')

            # i only need the credit score, so i extract that 
            credit_score = credit_score_result['CreditScore'].iloc[0]
            # round it to the nearets intger as it saved like that in the model
            credit_score=round(credit_score)

           # every thing that i need to dynmaically send to my template will be send through conext dictionary
            context = {
                'form': form,
                'credit_score': credit_score
            }
            return render(request, 'creditscore/result.html', context)
        else:
         
            context = {'form': form}
            return render(request, 'creditscore/result.html', context)
    else:
        
        form = CreditCardDataForm()
        context = {'form': form}
        return render(request, 'creditscore/Scoreboard.html', context)


def landingpage(request):
    # just rendering the landing page
    return render(request,'creditscore/LandingPage.html')


def loginpage(request):
    if request.method == "POST":
        # extracting he username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            # trying to see if the user's username exists in my DB
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, "creditscore/loginpage.html")  

        user = authenticate(request, username=username, password=password)
        # this auhenticte will securley cross chekc the username with the corresponding password

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect password")
            #if not then the password is clearly wrong

    return render(request, "creditscore/loginpage.html")



def RegisterPage(request):
    form = ExtendedUserCreationForm()
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        # i get the form from the user
        if form.is_valid():
            user = form.save()  
            # as i create the user i also have to set their profile details as they'll be an error on the profile page if i dont
            UserProfile.objects.create(  
                user=user,
                bank_balance=0,  
                current_bank="",  
                phone_number="",  
                
            )
            login(request, user)  
            return redirect('home')

    context = {'form': form}
    return render(request, 'creditscore/signUp.html', context)

def creditpay(request):
    return render(request,'creditscore/creditpayback.html')


@login_required(login_url='loginpage')
def save_credit_score(request):
    if request.method == 'POST':
        credit_score = request.POST.get('credit_score')

        # first Debug Check if credit_score was received
        if not credit_score:
            messages.error(request, "No credit score received.")
            return render(request, 'creditscore/result.html')

        try:
            # if it has been received, then convert to intger and save the score
            credit_score = int(credit_score)
            
            CreditScoreResult.objects.create(user=request.user, Score=credit_score)
            messages.success(request, 'Your credit score has been successfully saved!')
            return redirect('home')  
        except ValueError:
            
            messages.error(request, "Invalid credit score provided.")
            return render(request, 'creditscore/result.html')


    return render(request, 'creditscore/result.html')


def aboutpage(request):
    #render about page
    return render(request,'creditscore/AboutPage.html')

def contactpage(request):
    # render contact page
    return render(request,'creditscore/ContactPage.html')

@login_required(login_url='loginpage')
def homepage(request):
    # render homepage
    return render(request,'creditscore/homePage.html')


def logoutuser(request):
    #this will logout out the user, and the logout function will end their session
    logout(request)
    return redirect('landingpage')

def viewprofile(request):
    # retrive the corresponding users details
    user = request.user
    user_profile = user.profile

    # on their profile page i let the user see their most recent credit score, so i filter the Db to retreive the 3 most recent
    credit_scores = CreditScoreResult.objects.filter(user=user).order_by('-created')[:3]

    # the i filter once more to extract score from each entry
    recent_scores = [score.Score for score in credit_scores]

    # if ther is less than 3 entrys then fill the rest with Nones
    recent_scores.extend([None] * (3 - len(recent_scores)))

    context = {
        'user': user,
        'user_profile': user_profile,
        'recent_scores': recent_scores,
    }
    
    return render(request,'creditscore/userProfile.html',context)


@login_required(login_url='loginpage')
def editprofile(request):
    user = request.user
    profile = user.profile  # get user and profile info, knowing they have a 1-1 relationship

    if request.method == 'POST':
        user_form = ExtendedUserCreationForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        # Extracting the data from the user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        # Checking if the data for the user is valid
        if user_form.is_valid():
            user.save()
            messages.success(request, 'User information updated successfully!')
        
        # Check if profile is valid
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            
        return redirect('view-profile')  # Redirect to the profile view after upadate

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
    # get user details and profile info
    
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        # get the details from the form , also since its a picture i have to specify the instance
        if form.is_valid():
            form.save()
            return redirect('view-profile')  
    else:
        form = ProfileImageForm(instance=profile)

    context = {'form': form, 'profile': profile}
    return render(request, 'creditscore/editPhoto.html', context)


def credhist(request):
    #this will extract all the entries from my database under model creditscroreresult and order them from oldest to newest
    credit_score_results = CreditScoreResult.objects.filter(user=request.user).order_by('created')
    
    # Convert each 'created' datetime in 'credit_score_results' to a string format 'YYYY-MM-DD' and store them in a list.
    dates = [result.created.strftime('%Y-%m-%d') for result in credit_score_results]

    scores = [result.Score for result in credit_score_results]

    
    context = {
        'dates': dates,
        'scores': scores,
    }
    return render(request, 'creditscore/credHistory.html', context)


def saveloanscore(request):
    if request.method == 'POST':
        loan_score = request.POST.get('loan_score')
        if loan_score:
            try:
                loan_score = int(loan_score)
                LoanResult.objects.create(user=request.user, L_Score=loan_score)
                messages.success(request, 'Your loan score has been saved successfully!')
                return redirect('home')
            except ValueError:
                messages.error(request, 'Invalid score provided.')
                return redirect('save-loan')
        else:
            messages.error(request, 'No score was provided to save.')
            return redirect('save-loan')
    else:
        return render(request, 'creditscore/result2.html')

def credit_application_view(request):
    if request.method == 'POST':
        form = CreditApplicationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            credit_score = predict_user_credit_score(
                type_of_loan=cleaned_data['type_of_loan'],
                payment_behaviour=cleaned_data['payment_behaviour'],
                total_emi_per_month=cleaned_data['total_emi_per_month'],
                monthly_inhand_salary=cleaned_data['monthly_inhand_salary'],
                num_bank_accounts=cleaned_data['num_bank_accounts'],
                num_credit_cards=cleaned_data['num_credit_cards'],
                interest_rate=cleaned_data['interest_rate'],
                num_of_loan=cleaned_data['num_of_loan'],
                delay_from_due_date=cleaned_data['delay_from_due_date'],
                num_of_delayed_payment=cleaned_data['num_of_delayed_payment'],
                changed_credit_limit=cleaned_data['changed_credit_limit'],
                num_credit_inquiries=cleaned_data['num_credit_inquiries'],
                credit_mix=cleaned_data['credit_mix'],
                outstanding_debt=cleaned_data['outstanding_debt'],
                credit_utilization_ratio=cleaned_data['credit_utilization_ratio'],
                credit_history_age=cleaned_data['credit_history_age'],
                payment_of_min_amount=cleaned_data['payment_of_min_amount'],
                amount_invested_monthly=cleaned_data['amount_invested_monthly'],
            )

            # Pass the credit score to the template for display
            return render(request, 'creditscore/result2.html', {'credit_score': credit_score})
        else:
            # Return the form with errors
            return render(request, 'creditscore/Test101.html', {'form': form})
    else:
        # If not POST, create a new form instance
        form = CreditApplicationForm()
        return render(request, 'creditscore/Test101.html', {'form': form})