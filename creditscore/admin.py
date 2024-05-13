from django.contrib import admin
from .models import CreditCardData,CreditApplication,CreditScoreResult,UserProfile

# this will register all my models on the my django admin
admin.site.register(CreditCardData)
admin.site.register(CreditApplication)
admin.site.register(CreditScoreResult)
admin.site.register(UserProfile)