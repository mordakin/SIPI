from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):
    """Главная страница"""
    return HttpResponse('Hello')


def pageNotFound(request, exception):
    """Страница не найдена"""
    return HttpResponseNotFound('Такой страницы нет((')
