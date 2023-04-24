"""Create pages"""
import random

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib import messages


def index(request):
    """Главная страница"""
    return render(request, 'bank/index.html', {'title': 'Главная страница'})


# def accounts(request):
#     """Страница счетов"""
#     return render(request, 'bank/accounts.html', {'title': 'Счета'})
class AccountPage(CreateView):
    model = BankAccount
    fields = []
    template_name = 'bank/accounts.html'
    extra_context = {'title': 'Счета'}
    success_url = reverse_lazy('accounts')

    def form_valid(self, form):
        random_number = str(random.randint(1000000000, 9999999999))
        username = self.request.user
        form.instance.account_number = random_number
        form.instance.account_user = username
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all()
        return context


# class AccountListView(ListView):
#     model = BankAccount
#     template_name = 'bank/accounts.html'
#     context_object_name = 'object_list'
#
#     def get_queryset(self):
#         a = BankAccount.objects.filter(account_user=self.request.user)
#         print(a)
#         return BankAccount.objects.filter(account_user=self.request.user)


# def form_valid(self, form):
#     username = self.request.user
#     save_id_account = form.save()
#     print(save_id_account)
#     id_user = UserData.objects.filter(username=username)
#     print(id_user[0])
#     b = BankAccount.objects.filter(pk=getattr(save_id_account, 'id')).update(account_user=id_user[0])
#     # b = BankAccount.objects.update(account_user=id_user[0])
#
#     # self.request.session['account_user_id'] = str(user)
#     print(b)
#     # form.save()
#     return redirect('user_page')


def transfer(request):
    """Страницы переводов"""
    return render(request, 'bank/transfer.html', {'title': 'Переводы'})


def translation_history(request):
    """Страница истории переводов"""
    return render(request, 'bank/translation_history.html', {'title': 'История переводов'})


class LoginPage(LoginView):
    form_class = LoginUserForm
    template_name = 'bank/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('user_page')

    def form_invalid(self, form):
        form.add_error(None, "Неверный логин или пароль")
        return super().form_invalid(form)


class SingInPage(CreateView):
    form_class = RegisterUserForm
    template_name = 'bank/sing_in.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('user_page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('user_page')


def user_page(request):
    """Страница пользователя"""

    return render(request, 'bank/user_page.html', {'title': 'Мой аккаунт'})


def pageNotFound(request, exception):
    """Страница не найдена"""
    return HttpResponseNotFound('Такой страницы нет((')


def logout_user(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('login')
