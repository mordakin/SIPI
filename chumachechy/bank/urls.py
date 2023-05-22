"""Маршрутизация"""
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('accounts', AccountPage.as_view(), name='accounts'),
    path('accounts_delete/<int:pk>/delete/',
         AccountDelete.as_view(), name='accounts_delete'),
    path('transfer', TransferPage.as_view(), name='transfer'),
    path('translation_history', TranslationHistoryPage.as_view(),
         name='translation_history'),
    path('login', LoginPage.as_view(), name='login'),
    path('sing_in', SingInPage.as_view(), name='sing_in'),
    path('add', AccountAddCost.as_view(), name='add'),
    path('lost', AccountLostCost.as_view(), name='lost'),
    path('user_page', user_page, name='user_page'),
    path('logout', logout_user, name='logout'),

]
