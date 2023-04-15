"""Создание моделей(БД)"""
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class UserData(models.Model):
    """Данные пользователя"""
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField(
        validators=[MinValueValidator(80000000000), MaxValueValidator(89999999999), RegexValidator(
            regex='8[\d]+')], unique=True)
    passport = models.IntegerField(unique=True)
    fio = models.CharField(max_length=255, unique=True)


class BankAccount(models.Model):
    """Данные о счёте"""
    account_number = models.BigIntegerField(
        unique=True, null=True)  # номер счёта
    amount_of_funds = models.IntegerField(default=0)  # средств на счету
    account_user = models.ForeignKey('UserData', on_delete=models.PROTECT)


class Transfer(models.Model):
    """Данные о переводах"""
    sender_name = models.BigIntegerField()  # счёт отправителя
    recipient_name = models.BigIntegerField()  # счёт получателя
    cost = models.IntegerField  # сумма перевода
