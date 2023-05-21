"""Создание моделей(БД)"""
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class UserData(AbstractUser):
    """Данные пользователя"""
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField(unique=True)
    passport = models.IntegerField(unique=True)
    fio = models.CharField(max_length=255, unique=True)


class BankAccount(models.Model):
    """Данные о счёте"""
    account_number = models.IntegerField(
        unique=True, null=True)  # номер счёта
    amount_of_funds = models.IntegerField(default=0)  # средств на счету
    account_user = models.ForeignKey(
        'UserData', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.account_number)


class Transfer(models.Model):
    """Данные о переводах"""
    sender_name = models.BigIntegerField()  # счёт отправителя
    recipient_name = models.BigIntegerField()  # счёт получателя
    cost = models.IntegerField(default=0)  # сумма перевода
