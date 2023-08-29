import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View
from pytils.translit import slugify
from .forms import GuestForm, PasswordChangeCustomForm, CompanyProfileForm, RegisterForm1, RegisterForm2, RegisterForm3
from .models import CustomUser
from app_premises.models import Camp, Reservation, Favorite
from app_premises.forms import HolidayHouseForm

"""Разлогин, изменение пароля"""


class AnotherLogoutView(LogoutView):
    """ Стандартная форма разлогина от LogoutView """

    template_name = 'app_profiler/logout.html'


"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ ПРОФИЛЕЙ---"""


class AccountEditFromView(View):
    def get(self, request, slug):
        if not 'basic__register_button' in request.GET or request.user.slug == slug:
            current_user = CustomUser.objects.get(slug=slug)
            account_form = GuestForm(instance=current_user)
            change_password_form = PasswordChangeCustomForm(user=request.user.id)
            user_reservations = Reservation.objects.filter(guest=request.user.id)
            favorite_list = Favorite.objects.filter(user=request.user.id).prefetch_related('camps', 'flats')

            return render(request, 'app_profiler/user_detail.html',
                          context={
                              'account_form': account_form,
                              'slug': slug,
                              'current_user': current_user,
                              'change_password_form': change_password_form,
                              'user_reservations': user_reservations,
                              'favorite_list': favorite_list,
                          }
                          )
        else:
            return redirect('app_profiler:account_detail', slug=request.user.slug)

    def post(self, request, slug):
        current_user = CustomUser.objects.get(slug=slug)
        account_form = GuestForm(request.POST, instance=current_user)
        user_reservations = Reservation.objects.filter(guest=request.user.id)
        change_password_form = PasswordChangeCustomForm(user=request.user.id)
        favorite_list = Favorite.objects.filter(user=request.user.id).prefetch_related('camps', 'flats')

        if 'account__save_form' in request.POST and account_form.is_valid():
            account = account_form.save(commit=False)
            account.telegram = account_form.cleaned_data['telegram']
            account.save(update_fields=["telegram"])

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
                account.save(update_fields=["slug"])
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
                          'favorite_list': favorite_list,
                      }
                      )


class AccountReservationListView(View):
    def get(self, request, slug):
        user_reservations = Reservation.objects.filter(guest=request.user.id)
        return render(request, 'app_profiler/user_reservation_list.html',
                      context={'user_reservations': user_reservations, })

    def post(self, request, slug):
        if 'user_reservation_list__discard' in request.POST:
            reservation_id = request.POST.get('user_reservation_list__discard')
            current_reservation = Reservation.objects.get(id=reservation_id)
            if current_reservation.realty.realty_book_count > 0:
                current_reservation.realty.realty_book_count -= 1
                current_reservation.is_booked = False
                current_reservation.is_canceled = True
                current_reservation.canceled_at = datetime.datetime.now()
                current_reservation.save()

        user_reservations = Reservation.objects.filter(guest=request.user.id)
        return render(request, 'app_profiler/user_reservation_list.html',
                      context={'user_reservations': user_reservations})


class CompanyEditFromView(View):
    def get(self, request, company_id):
        if company_id == request.user.id:
            current_company = CustomUser.objects.get(id=company_id)
            company_id = current_company.id
            company_form = CompanyProfileForm(instance=current_company)
            realty_form = HolidayHouseForm()
            return render(request, 'app_profiler/edit_company.html',
                          context={
                              'company_form': company_form,
                              'company_id': company_id,
                              'current_company': current_company,
                              'realty_form': realty_form,
                          }
                          )

        else:
            return redirect('app_profiler:company_detail', company_id=request.user.id)

    def post(self, request, company_id):
        current_company = CustomUser.objects.get(id=company_id)
        company_form = CompanyProfileForm(request.POST, instance=current_company)
        realty_form = HolidayHouseForm(request.POST)
        if 'account__save_form' in request.POST:
            if company_form.is_valid():
                company = company_form.save(commit=False)
                company.type = company_form.cleaned_data['type']
                company.middle_name = company_form.cleaned_data['middle_name']
                company.save()
                return redirect('app_profiler:company_detail', company_id=company_id)
            else:
                messages.error(request, 'Ошибка при изменении ссылки на компанию')
            return redirect('app_profiler:company_detail', company_id=company_id)

        if 'account__save_realty_object' in request.POST and realty_form.is_valid():
            realty = realty_form.save(commit=False)
            realty.company = realty_form.cleaned_data['company']
            realty.slug = slugify(realty_form.cleaned_data['realty_name'])
            realty.realty_book_count = 0
            realty.save()
            realty_form.save_m2m()
            # for photo in files:
            #     Photos.objects.create(realty_obj=realty.id, photo=photo)

        return render(request, 'app_profiler/edit_company.html',
                      context={
                          'company_form': company_form,
                          'company_id': company_id,
                          'current_company': current_company,
                          'realty_form': realty_form}
                      )


""" КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ ПРОФИЛЕЙ """


def register_step1(request):
    """ Форма регистрации пользователя шаг 1 """
    if not request.user.is_authenticated:
        register_form = RegisterForm1()
        if request.method == 'GET':
            return render(request, 'app_profiler/register1.html', {'register_form': register_form})

        if request.method == "POST":
            last_user = CustomUser.objects.last()
            register_form = RegisterForm1(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.slug = slugify(f'user{last_user.id + 1}')
                user.is_active = True
                email = register_form.cleaned_data.get('email')
                raw_password = register_form.cleaned_data.get('password1')
                user.save()
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                return redirect('app_profiler:register2')
            return render(request, 'app_profiler/register1.html', context={'register_form': register_form})
        return render(request, 'app_profiler/register1.html', context={'register_form': register_form})
    else:
        return redirect('app_index:index')


def register_step2(request):
    """ Регистрация пользователя шаг 2 """

    current_user = CustomUser.objects.get(id=request.user.id)
    register_form = RegisterForm2()
    if request.method == 'GET':
        return render(request, 'app_profiler/register2.html', {'register_form': register_form})

    if request.method == "POST":
        register_form = RegisterForm2(request.POST)
        if register_form.is_valid():
            current_user.first_name = register_form.cleaned_data['first_name']
            current_user.last_name = register_form.cleaned_data['last_name']
            current_user.phone = register_form.cleaned_data['phone']
            current_user.slug = register_form.cleaned_data['slug']
            current_user.birthday = register_form.cleaned_data['birthday']
            current_user.save()
            return redirect('app_profiler:register3')
        return render(request, 'app_profiler/register2.html', context={'register_form': register_form})
    return render(request, 'app_profiler/register2.html', context={'register_form': register_form})


def register_step3(request):

    current_user = CustomUser.objects.get(id=request.user.id)
    register_form = RegisterForm3()
    if request.method == 'GET':
        return render(request, 'app_profiler/register3.html', {'register_form': register_form})

    if request.method == "POST":
        register_form = RegisterForm3(request.POST)
        if register_form.is_valid():
            current_user.is_company = register_form.cleaned_data['is_company']
            current_user.is_active = register_form.cleaned_data['is_active']
            current_user.save()
            return redirect('app_profiler:account_detail', slug=current_user.slug)
        return render(request, 'app_profiler/register3.html', context={'register_form': register_form})
    return render(request, 'app_profiler/register3.html', context={'register_form': register_form})
