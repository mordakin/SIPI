"""Create pages"""
import random

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Q, F
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from .forms import *
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView, UpdateView
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

    def get_form_kwargs(self):
        """Добавляем дополнительный аргумент user в словарь kwargs """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

    def form_valid(self, form):
        """Проверка не заблокирован ли пользователь"""
        username = form.cleaned_data['username']
        user = UserData.objects.get(username=username)

        if user.block:
            messages.error(self.request, "Ваш аккаунт заблокирован")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        """Вывод при неверном пароле"""
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


class AccountAddCost(CreateView):
    """Страница пополнения"""
    form_class = AddedForm
    template_name = 'bank/add.html'
    extra_context = {'title': 'Пополнение'}
    success_url = reverse_lazy('add')

    def get_form_kwargs(self):
        """Добавляем дополнительный аргумент user в словарь kwargs """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Пополнение"""
        sender_name = form.cleaned_data['sender_name']
        cost = form.cleaned_data['cost']
        if cost < 0:
            messages.error(self.request, "Сумма должна быть положительной!")
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        else:
            BankAccount.objects.filter(account_number=sender_name).update(
                amount_of_funds=F('amount_of_funds') + cost)
            messages.success(self.request, "Пополнение прошло успешно")
            # transfer = Transfer(sender_name=sender_name, recipient_name=sender_name, cost=cost)
            # transfer.save()
            form.instance.sender_name = sender_name
            form.instance.recipient_name = sender_name
            form.instance.cost = cost
            return super().form_valid(form)


class AccountLostCost(CreateView):
    """Страница снятия"""
    form_class = AddedForm
    template_name = 'bank/lost.html'
    extra_context = {'title': 'Снятие'}
    success_url = reverse_lazy('user_page')

    def get_form_kwargs(self):
        """Добавляем дополнительный аргумент user в словарь kwargs """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Снятие"""
        sender_name = form.cleaned_data['sender_name']
        cost = form.cleaned_data['cost']
        if cost < 0:
            messages.error(self.request, "Сумма должна быть положительной!")
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        elif BankAccount.objects.get(account_number=sender_name).amount_of_funds - cost < 0:
            messages.error(self.request, "У вас нет столько денег")
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        else:
            BankAccount.objects.filter(account_number=sender_name).update(
                amount_of_funds=F('amount_of_funds') - cost
            )
            return super().form_invalid(form)


class BlockUser(View):
    """Страница блокировки аккаунта"""
    template_name = 'bank/user_page.html'
    extra_context = {'title': 'Главная страница'}
    success_url = reverse_lazy('logout')

    def get(self, request, *args, **kwargs):
        """Переопределеие гет запроса"""
        return render(request, self.template_name, self.extra_context)

    def post(self, request, *args, **kwargs):
        """Переопределеие пост запроса"""
        user = request.user
        user.block = True  # Измените значение поля block на True (1)
        user.save()  # Сохраните изменения в базе данных
        return redirect(self.success_url)


def pageNotFound(request, exception):
    """Страница не найдена"""
    return HttpResponseNotFound('Такой страницы нет((')


def logout_user(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('login')
