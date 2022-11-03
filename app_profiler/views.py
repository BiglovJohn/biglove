from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View
from requests import put

from .forms import GuestForm, PasswordChangeCustomForm
from .models import CustomUser
from app_premises.models import RealtyObject, Reservation

"""Разлогин, изменение пароля"""


class AnotherLogoutView(LogoutView):
    template_name = 'app_profiler/logout.html'


"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ ПРОФИЛЕЙ---"""


class AccountEditFromView(View):
    def get(self, request, user_id):
        current_user = CustomUser.objects.get(id=user_id)
        account_form = GuestForm(instance=current_user)
        change_password_form = PasswordChangeCustomForm(user=request.user.id)
        user_reservations = Reservation.objects.filter(guest=user_id)

        return render(request, 'app_profiler/user_detail.html',
                      context={
                          'account_form': account_form,
                          'user_id': user_id,
                          'current_user': current_user,
                          'change_password_form': change_password_form,
                          'user_reservations': user_reservations,
                      }
                      )

    def post(self, request, user_id):
        current_user = CustomUser.objects.get(id=user_id)
        account_form = GuestForm(request.POST, instance=current_user)
        user_reservations = Reservation.objects.filter(guest=user_id)
        change_password_form = PasswordChangeCustomForm(user=user_id)

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
                    return redirect('app_profiler:account_detail', user_id=user_id)
                else:
                    messages.error(request, 'Please correct the error below.')
            else:
                change_password_form = PasswordChangeCustomForm(request.user)
            return render(request, 'app_profiler/user_detail.html', {
                'change_password_form': change_password_form
            })
        return render(request, 'app_profiler/user_detail.html',
                      context={
                          'account_form': account_form,
                          'user_id': user_id,
                          'current_user': current_user,
                          'change_password_form': change_password_form,
                          'user_reservations': user_reservations,
                      }
                      )


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""
