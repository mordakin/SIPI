"""Формы для отправки данных"""
from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddUser(forms.ModelForm):
    """Класс для формы регистарции"""
    class Meta:
        """Класс наследования от модели"""
        model = UserData
        fields = ['username', 'password', 'phone_number', 'passport', 'fio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'passport': forms.NumberInput(attrs={'class': 'form-control'}),
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
        }

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


class LoginUser(forms.ModelForm):
    """Класс для формы авторизации"""
    class Meta:
        """Класс наследования от модели"""
        model = UserData
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }
