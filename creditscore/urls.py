from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('scorecard', views.creditscore, name="Scorecard"),
    path('', views.landingpage, name="landingpage"),
    path('loginpage', views.loginpage, name="loginpage"),
    path('form2', views.credit_score_view, name="creditscore"),
    path('signup', views.RegisterPage, name="signup"),
    path('creditpay', views.creditpay, name="creditpay"),
    path('save-credit', views.save_credit_score, name="saveCredit1"),
    path('about', views.aboutpage, name="about"),
    path('contact', views.contactpage, name="contact"),
    path('home', views.homepage, name="home"),
    path('logout', views.logoutuser, name='logout'),
    path('logout', views.logoutuser, name='logout'),
    path('profile', views.viewprofile, name='view-profile'),
    path('edit', views.editprofile, name='edit-profile'),
    path('edit-photo', views.editprofileimage, name='edit-photo'),
    path('credit-history', views.credhist, name='credit-history'),
]
