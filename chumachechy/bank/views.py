"""Create pages"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *


def index(request):
    """Главная страница"""
    return render(request, 'bank/index.html', {'title': 'Главная страница'})


def accounts(request):
    """Страница счетов"""
    return render(request, 'bank/accounts.html', {'title': 'Счета'})


def transfer(request):
    """Страницы переводов"""
    return render(request, 'bank/transfer.html', {'title': 'Переводы'})


def translation_history(request):
    """Страница истории переводов"""
    return render(request, 'bank/translation_history.html', {'title': 'История переводов'})


def login(request):
    """Авторизация"""
    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = LoginUser()
    return render(request, 'bank/login.html', {'title': 'Вход', 'form': form})


def sing_in(request):
    """Регистрация"""
    if request.method == 'POST':
        form = AddUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    else:
        form = AddUser()
    return render(request, 'bank/sing_in.html', {'title': 'Регистрация', 'form': form})


def user_page(request):
    """Страница пользователя"""
    return render(request, 'bank/user_page.html', {'title': 'Мой аккаунт'})


def pageNotFound(request, exception):
    """Страница не найдена"""
    return HttpResponseNotFound('Такой страницы нет((')
