from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class CreditCardData(models.Model):
    LIMIT_BAL = models.FloatField()
    SEX = models.IntegerField()
    EDUCATION = models.FloatField()
    MARRIAGE = models.FloatField()
    AGE = models.FloatField()
    PAY_0 = models.FloatField()
    PAY_2 = models.FloatField()
    PAY_3 = models.FloatField()
    PAY_4 = models.FloatField()
    PAY_5 = models.FloatField()
    PAY_6 = models.FloatField()
    BILL_AMT1 = models.FloatField()
    BILL_AMT2 = models.FloatField()
    BILL_AMT3 = models.FloatField()
    BILL_AMT4 = models.FloatField()
    BILL_AMT5 = models.FloatField()
    BILL_AMT6 = models.FloatField()
    PAY_AMT1 = models.FloatField()
    PAY_AMT2 = models.FloatField()
    PAY_AMT3 = models.FloatField()
    PAY_AMT4 = models.FloatField()
    PAY_AMT5 = models.FloatField()
    PAY_AMT6 = models.FloatField()
    label = models.IntegerField()
   

    def __str__(self):
        return f"CreditCardData(ID: {self.id}, Label: {self.label})"
    
class CreditApplication(models.Model):
    type_of_loan = models.CharField(max_length=100)
    payment_behaviour = models.CharField(max_length=100)
    total_emi_per_month = models.FloatField()
    monthly_inhand_salary = models.FloatField()
    num_bank_accounts = models.IntegerField()
    num_credit_cards = models.IntegerField()
    interest_rate = models.FloatField()
    num_of_loan = models.CharField(max_length=10)
    delay_from_due_date = models.IntegerField()
    num_of_delayed_payment = models.CharField(max_length=10)
    changed_credit_limit = models.CharField(max_length=3)
    num_credit_inquiries = models.FloatField()
    credit_mix = models.FloatField()
    outstanding_debt = models.FloatField()
    credit_utilization_ratio = models.FloatField()
    credit_history_age = models.CharField(max_length=20)
    payment_of_min_amount = models.CharField(max_length=3)
    amount_invested_monthly = models.FloatField()


class CreditScoreResult(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Score= models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bank_balance = models.IntegerField(null=True, blank=True)
    current_bank = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png') 

    def __str__(self):
        return self.user.username
    
class LoanResult(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    L_Score=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)


    
    




