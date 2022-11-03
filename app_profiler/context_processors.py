from app_profiler.forms import AuthForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from requests import put

from .forms import GuestForm, PasswordChangeCustomForm
from .models import CustomUser


def render_login_form(request):
    if 'submit-login-form' in request.POST:
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            email = auth_form.cleaned_data['email']
            password = auth_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                else:
                    auth_form.add_error('__all__', 'Проверьте правильность введёных данных')
    else:
        auth_form = AuthForm()

    return {'auth_form': auth_form}


def render_register_form(request):
    """Регистрация и авторизация"""
    if 'save-register-form' in request.POST:
        register_form = RegisterForm(request.POST)
        user_obj = CustomUser()
        if register_form.is_valid():
            user = register_form.save()
            last_name = register_form.cleaned_data.get('last_name')
            first_name = register_form.cleaned_data.get('first_name')
            phone = register_form.cleaned_data.get('phone')
            email = register_form.cleaned_data.get('email')
            raw_password = register_form.cleaned_data.get('password1')
            is_active = register_form.cleaned_data.get('is_active')
            is_company = register_form.cleaned_data.get('is_company')

            user = authenticate(email=email, password=raw_password)
            login(request, user)
    else:
        register_form = RegisterForm()
    return {'register_form': register_form}


# def render_profile_detail_view(request):
#     if request.user.is_authenticated:  # and request.META['PATH_INFO'] == '/'
#         if request.user.is_company:
#             if request.method == 'GET':
#                 profile = ManagerProfile.objects.get(referring_user=request.user.id)
#                 # manager = ManagerProfile.objects.get(referring_user=profile[0].id)
#                 manager_form = ManagerProfileForm(instance=profile)
#                 return {'profile': profile, 'manager_form': manager_form}
#
#             if 'save-manager-form' in request.POST:
#                 profile = ManagerProfile.objects.get(referring_user=request.user.id)
#                 # manager = ManagerProfile.objects.get(referring_user=profile[0].id)
#                 manager_form = ManagerProfileForm(request.POST, instance=profile)
#                 if manager_form.is_valid():
#                     profile = manager_form.save(commit=False)
#                     profile.save()
#
#                 return {'profile': profile, 'manager_form': manager_form}
#     profile = ManagerProfile.objects.none()
#     return {'profile': profile}


def render_guest_detail_view(request):
    if request.user.is_authenticated:

        if request.method == 'GET':
            guest = CustomUser.objects.get(id=request.user.id)
            guest_form = GuestForm(instance=guest)
            return {'guest': guest, 'guest_form': guest_form}

        if 'save-edit-guest' in request.POST:
            guest = CustomUser.objects.get(id=request.user.id)
            # manager = ManagerProfile.objects.get(referring_user=profile[0].id)
            guest_form = GuestForm(request.POST, instance=guest)

            if guest_form.is_valid():
                guest.save()

            return {'guest': guest, 'guest_form': guest_form}

        guest = CustomUser.objects.get(id=request.user.id)
        return {'guest': guest}

    guest = CustomUser.objects.none()
    return {'guest': guest}


# def render_change_password(request):
#     if request.method == 'GET':
#         change_password_form = PasswordChangeCustomForm(user=request.user.id)
#         return {'change_password_form': change_password_form}
#
#     if 'account__change_password_form' in request.POST:
#         change_password_form = PasswordChangeCustomForm(user=request.user.id, data=put)
#         if change_password_form.is_valid():
#             change_password_form.save()  # Добавить сообщение об удачной смене пароля
#         return {'change_password_form': change_password_form}
#     else:
#         change_password_form = PasswordChangeCustomForm(user=request.user.id)
#         return {'change_password_form': change_password_form}
