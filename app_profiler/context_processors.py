from app_profiler.forms import AuthForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from .forms import GuestForm
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
        print(auth_form.errors)
    else:
        auth_form = AuthForm()

    return {'auth_form': auth_form}


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


def render_current_company_slug(request):
    if request.user.is_authenticated:
        if request.user.is_company:
            current_company = CustomUser.objects.get(id=request.user.id)
            company_slug = current_company.slug
            return {'company_slug': company_slug}
        else:
            company_slug = None
            return {'company_slug': company_slug}
    else:
        company_slug = None
        return {'company_slug': company_slug}


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
