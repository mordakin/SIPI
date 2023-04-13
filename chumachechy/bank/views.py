"""Create pages"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


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
    return render(request, 'bank/login.html', {'title': 'Вход'})


def sing_in(request):
    """Регистрация"""
    return render(request, 'bank/sing_in.html', {'title': 'Регистрация'})


def pageNotFound(request, exception):
    """Страница не найдена"""
    return HttpResponseNotFound('Такой страницы нет((')
