from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):
    return HttpResponse('Hello')


def pageNotFound(request, exception):
    return HttpResponseNotFound('Такой страницы нет((')
