"""Маршрутизация"""
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('accounts', AccountPage.as_view(), name='accounts'),
    path('transfer', transfer, name='transfer'),
    path('translation_history', translation_history, name='translation_history'),
    path('login', LoginPage.as_view(), name='login'),
    path('sing_in', SingInPage.as_view(), name='sing_in'),
    path('user_page', user_page, name='user_page'),
    path('logout', logout_user, name='logout'),

]
