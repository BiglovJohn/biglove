from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View
from requests import put

from .forms import GuestForm, PasswordChangeCustomForm
from .models import CustomUser
from app_premises.models import HolidayHouseObject, Reservation

"""Разлогин, изменение пароля"""


class AnotherLogoutView(LogoutView):
    template_name = 'app_profiler/logout.html'


"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ ПРОФИЛЕЙ---"""


class AccountEditFromView(View):
    def get(self, request, slug):
        if request.user.slug == slug:
            current_user = CustomUser.objects.get(slug=slug)
            account_form = GuestForm(instance=current_user)
            change_password_form = PasswordChangeCustomForm(user=request.user.id)
            user_reservations = Reservation.objects.filter(guest=request.user.id)

            return render(request, 'app_profiler/user_detail.html',
                          context={
                              'account_form': account_form,
                              'slug': slug,
                              'current_user': current_user,
                              'change_password_form': change_password_form,
                              'user_reservations': user_reservations,
                          }
                          )
        else:
            return redirect('app_profiler:account_detail', slug=request.user.slug)

    def post(self, request, slug):
        current_user = CustomUser.objects.get(slug=slug)
        account_form = GuestForm(request.POST, instance=current_user)
        user_reservations = Reservation.objects.filter(guest=request.user.id)
        change_password_form = PasswordChangeCustomForm(user=request.user.id)

        if 'account__save_form' in request.POST and account_form.is_valid():
            account = account_form.save(commit=False)
            account.save()

        if 'account__change_password_form' in request.POST:
            if request.method == 'POST':
                change_password_form = PasswordChangeCustomForm(request.user, request.POST)
                if change_password_form.is_valid():
                    user = change_password_form.save()
                    update_session_auth_hash(request, user)  # Important!
                    messages.success(request, 'Your password was successfully updated!')
                    return redirect('app_profiler:account_detail', slug=slug)
                else:
                    messages.error(request, 'Please correct the error below.')
            else:
                change_password_form = PasswordChangeCustomForm(request.user)
            return render(request, 'app_profiler/user_detail.html', {
                'change_password_form': change_password_form
            })

        if 'account__change_slug' in request.POST:
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.slug = account_form.cleaned_data['slug']
                account.save()
                return redirect('app_profiler:account_detail', slug=slug)
            else:
                messages.error(request, 'Ошибка при изменении ника')
            return redirect('app_profiler:account_detail', slug=slug)

        return render(request, 'app_profiler/user_detail.html',
                      context={
                          'account_form': account_form,
                          'slug': slug,
                          'current_user': current_user,
                          'change_password_form': change_password_form,
                          'user_reservations': user_reservations,
                      }
                      )


class AccountReservationListView(View):
    def get(self, request, slug):
        user_reservations = Reservation.objects.filter(guest=request.user.id)
        return render(request, 'app_profiler/user_reservation_list.html', context={'user_reservations': user_reservations, })

    def post(self, request, slug):
        user_reservations = Reservation.objects.filter(guest=request.user.id)
        return render(request, 'app_profiler/user_reservation_list.html', context={'user_reservations': user_reservations, })


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""
