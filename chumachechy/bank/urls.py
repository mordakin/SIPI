"""Маршрутизация"""
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('accounts', accounts, name='accounts'),
    path('transfer', transfer, name='transfer'),
    path('translation_history', translation_history, name='translation_history'),
    path('login', login, name='login'),
    path('sing_in', sing_in, name='sing_in'),

]
