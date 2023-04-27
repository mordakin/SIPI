"""Формы для отправки данных"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class RegisterUserForm(UserCreationForm):
    """Класс для формы регистарции"""
    username = forms.CharField(max_length=255, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(
        label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport = forms.IntegerField(label='Серия и номер пасспорта', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    fio = forms.CharField(label='ФИО', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', max_length=255,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторение пароля', max_length=255,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        """Класс наследования от модели"""
        model = UserData
        fields = ['username', 'phone_number',
                  'passport', 'fio', 'password1', 'password2']

    def clean_passport(self):
        """Валидатор пасспорта"""
        passport = self.cleaned_data['passport']
        if passport > 9999999999 or passport < 1000000000:
            raise ValidationError(
                'В номере пасспорта должно быть ровно 10 цифр')
        return passport

    def clean_phone_number(self):
        """Валидатор телефона"""
        phone_number = self.cleaned_data['phone_number']
        test_first_figure = str(phone_number)[0]
        test_length = str(phone_number)
        if test_first_figure != '8' or len(test_length) != 11:
            raise ValidationError(
                'Номер должен начинаться с 8 и иметь 10 цифр после этого')
        return phone_number

    def clean_fio(self):
        """Валидатор ФИО"""
        fio = self.cleaned_data['fio']
        count_space = fio.count(' ')
        if (any(x.isalpha() for x in fio)
                and any(x.isspace() for x in fio)
                and all(x.isalpha() or x.isspace() for x in fio)
                and count_space == 2):
            return fio
        else:
            raise ValidationError(
                'В ФИО могут быть только буквы и фио состоит из трёх слов разделённых пробелом')


class LoginUserForm(AuthenticationForm):
    """Класс для формы авторизации"""
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class TransferForm(forms.ModelForm):
    sender_name = forms.IntegerField(label='Счёт с которого хотите отправить деньги',
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    recipient_name = forms.IntegerField(label='Счёт на который хотите отправить деньги',
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cost = forms.IntegerField(label='Сумма перевода',
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Transfer
        fields = ['sender_name', 'recipient_name', 'cost']
# class BankAccountForm(forms.ModelForm):
#     account_number = forms.IntegerField(label='Номер счёта', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     amount_of_funds = forms.IntegerField(label='Количество средств',
#                                          widget=forms.TextInput(attrs={'class': 'form-control'}))

# class Meta:
#     model = BankAccount
#     fields = ['account_number', 'amount_of_funds']
