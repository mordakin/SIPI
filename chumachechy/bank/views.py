"""Create pages"""
import random

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView
from django.contrib import messages


def index(request):
    """Главная страница"""
    return render(request, 'bank/index.html', {'title': 'Главная страница'})


class AccountPage(CreateView):
    """Страница счетов(создание и отображение)"""
    model = BankAccount
    fields = []
    template_name = 'bank/accounts.html'
    extra_context = {'title': 'Счета'}
    success_url = reverse_lazy('accounts')

    def form_valid(self, form):
        """Генерация номера счёта"""
        random_number = str(random.randint(1000000000, 9999999999))
        username = self.request.user
        form.instance.account_number = random_number
        form.instance.account_user = username
        messages.success(self.request, f'Счет {random_number} успешно создан.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Отображение счетов пользователя"""
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(
            account_user_id=self.request.user)
        return context


class AccountDelete(DeleteView):
    """Страница счетов (удаление)"""
    model = BankAccount
    template_name = 'bank/accounts.html'
    success_url = reverse_lazy('accounts')

    def form_valid(self, form):
        """Проверка на наличие средств перед удалением"""
        if self.object.amount_of_funds > 0:
            messages.error(self.request,
                           f'Не удалось удалить счет {self.object.account_number}, так как на нем есть деньги. '
                           'Переведите деньги на другой счёт или снимите все деньги')
            return redirect('accounts')
        else:
            messages.success(
                self.request, f'Счет {self.object.account_number} успешно удален.')
            return super().form_valid(form)


class TransferPage(CreateView):
    """Страница переводов"""
    form_class = TransferForm
    template_name = 'bank/transfer.html'
    extra_context = {'title': 'Переводы'}
    success_url = reverse_lazy('transfer')

    def form_valid(self, form):
        """Проверка введённых данных"""
        sender_name_field = form.cleaned_data[
            'sender_name']  # берём значение из формы (счёт отправителя)
        # берём значение из формы (счёт получателя)
        recipient_name_field = form.cleaned_data['recipient_name']
        # берём значение из формы (сумма перевода)
        cost_field = form.cleaned_data['cost']
        sender_account = BankAccount.objects.filter(account_user_id=self.request.user,
                                                    account_number=sender_name_field)  # смотрим что есть такой счёт и у данного пользователя
        recipient_account = BankAccount.objects.filter(
            account_number=recipient_name_field)  # ищем счёт получателя
        if sender_account and recipient_account and cost_field > 0:
            recipient_amount = recipient_account.first(
            ).amount_of_funds  # количество средств получателя
            # количество средств отправителя
            sender_amount = sender_account.first().amount_of_funds
            if sender_amount - cost_field >= 0:
                BankAccount.objects.filter(account_number=recipient_name_field).update(
                    amount_of_funds=recipient_amount + cost_field)  # прибавляем к имющимся деньгам сумму перевода
                BankAccount.objects.filter(account_number=sender_name_field).update(
                    amount_of_funds=sender_amount - cost_field)  # отнимаем сумму перевода
                messages.success(self.request, "Перевод успешно выполнен")
                return super().form_valid(form)  # вызов оригинального метода form_valid
            else:
                messages.error(
                    self.request, f"На счету {sender_name_field} недостаточно средств")
                context = self.get_context_data(form=form)
                return self.render_to_response(context)
        elif not sender_account:
            messages.error(
                self.request, f"У вас нет счёта {sender_name_field}")
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        elif not recipient_account:
            messages.error(
                self.request, f"Нет получателя с номером счёта {recipient_name_field}")
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        else:
            messages.error(self.request, "Сумма должна быть положительной!")
            context = self.get_context_data(form=form)
            return self.render_to_response(context)


class TranslationHistoryPage(CreateView):
    """Страница истории переводов"""
    model = Transfer
    fields = []
    template_name = 'bank/translation_history.html'
    extra_context = {'title': 'История переводов'}
    success_url = reverse_lazy('transfer')

    def get_context_data(self, **kwargs):
        """Отображение переводов"""
        context = super().get_context_data(**kwargs)
        take_account_user = BankAccount.objects.filter(account_user=self.request.user).values_list('account_number',
                                                                                                   flat=True)
        context["transfer1"] = Transfer.objects.filter(
            Q(sender_name__in=take_account_user) | Q(recipient_name__in=take_account_user))
        return context


class LoginPage(LoginView):
    """Страница авторизации"""
    form_class = LoginUserForm
    template_name = 'bank/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        """Ссылка перехода"""
        return reverse_lazy('user_page')

    def form_invalid(self, form):
        """Вывод при неверном пароле"""
        form.add_error(None, "Неверный логин или пароль")
        return super().form_invalid(form)


class SingInPage(CreateView):
    """Страница регистрации"""
    form_class = RegisterUserForm
    template_name = 'bank/sing_in.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('user_page')

    def form_valid(self, form):
        """Внос данных в бд"""
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
