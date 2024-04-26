from django.contrib import admin
from .models import CreditCardData,CreditApplication,CreditScoreResult,UserProfile


admin.site.register(CreditCardData)
admin.site.register(CreditApplication)
admin.site.register(CreditScoreResult)
admin.site.register(UserProfile)