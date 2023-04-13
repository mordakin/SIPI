"""Create pages"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):
    """Главная страница"""
    return render(request, 'bank/index.html', {'title': 'Главная страница'})


def pageNotFound(request, exception):
    """Страница не найдена"""
    return HttpResponseNotFound('Такой страницы нет((')
