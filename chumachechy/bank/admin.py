"""Админка"""
from django.contrib import admin

from .models import *

admin.site.register(UserData)
admin.site.register(BankAccount)
admin.site.register(Transfer)
