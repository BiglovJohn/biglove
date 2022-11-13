import datetime
import os

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from app_premises.models import Reservation, RealtyOptions, HolidayHouseObject
from app_premises.forms import ReservationForm, PriseFilterForm, DropdownFilterForm, RealtyTypeCheckBoxForm, \
    OptionFilterForm, InRoomOptionFilterForm, FoodOptionFilterForm, HolidayHouseForm, PhotosForm, BookCancelForm, \
    PayTypeForm

from app_profiler.models import CustomUser
from app_profiler.forms import RegisterForm, AuthForm
from app_comments.forms import CommentsForm
from app_companies.models import CompanyProfile

from .forms import DropdownFilterLongTermForm, AreaFilterForm, FloorFilterForm, RulesFilterForm, BathroomFilterForm, \
    FurnitureFilterForm, TechniqueFilterForm, LongTermRentObjectForm
from .models import LongTermRentObject, LongTermPhotos
from app_premises.views import permission_denied


def main_lt_realty_list(request):
    """
        Получаем параметры с index.html форм и по ним фильтруем поисковую выдачу:
        - Страна
        - Город
    """

    if 'lt_realty_list__search' in request.POST:
        query = request.POST.get('lt')

        lt_realty_list = LongTermRentObject.objects.filter(
            Q(realty_country__iregex=query) | Q(realty_city__iregex=query) | Q(
                realty_region__iregex=query)).prefetch_related('furniture').prefetch_related('technique')

        """ Фильтрация по цене и дате размещения """
        main_filter = DropdownFilterLongTermForm(request.POST)
        if main_filter.is_valid():
            if main_filter.cleaned_data['filter_param'] == 'i':
                lt_realty_list = lt_realty_list.order_by('realty_price')

            if main_filter.cleaned_data['filter_param'] == 'x':
                lt_realty_list = lt_realty_list.order_by('-realty_price')

            if main_filter.cleaned_data['filter_param'] == 'p':
                lt_realty_list = lt_realty_list.order_by('-updated_at')

        """ Фильтрация по диапазону цен """
        price_filter = PriseFilterForm(request.POST)
        if price_filter.is_valid():
            if price_filter.cleaned_data['min_price']:
                lt_realty_list = lt_realty_list.filter(realty_price__gte=price_filter.cleaned_data['min_price'])

            if price_filter.cleaned_data['max_price']:
                lt_realty_list = lt_realty_list.filter(realty_price__lte=price_filter.cleaned_data['max_price'])

        """ Фильтрация по диапазону площадей """
        area_filter = AreaFilterForm(request.POST)
        if area_filter.is_valid():
            if area_filter.cleaned_data['min_area']:
                lt_realty_list = lt_realty_list.filter(realty_area__gte=area_filter.cleaned_data['min_area'])

            if area_filter.cleaned_data['max_area']:
                lt_realty_list = lt_realty_list.filter(realty_area__lte=area_filter.cleaned_data['max_area'])

        """ Фильтрация по диапазону этажей """
        floor_filter = FloorFilterForm(request.POST)
        if floor_filter.is_valid():
            if floor_filter.cleaned_data['min_floor']:
                lt_realty_list = lt_realty_list.filter(floor__gte=floor_filter.cleaned_data['min_floor'])

            if floor_filter.cleaned_data['max_floor']:
                lt_realty_list = lt_realty_list.filter(floor__lte=floor_filter.cleaned_data['max_floor'])

        """ Фильтрация по правилам """
        rules_checkbox = RulesFilterForm(request.POST)

        if rules_checkbox.is_valid():
            if not rules_checkbox.cleaned_data['rule_option']:
                pass
            if '1' in rules_checkbox.cleaned_data['rule_option']:
                lt_realty_list = lt_realty_list.filter(children=True)
            if '2' in rules_checkbox.cleaned_data['rule_option']:
                lt_realty_list = lt_realty_list.filter(animals=True)
            if '3' in rules_checkbox.cleaned_data['rule_option']:
                lt_realty_list = lt_realty_list.filter(smoke=True)

        """ Фильтрация по санузлу """
        bathroom_checkbox = BathroomFilterForm(request.POST)

        if bathroom_checkbox.is_valid():
            if not bathroom_checkbox.cleaned_data['bathroom_option']:
                pass
            if '1' in bathroom_checkbox.cleaned_data['bathroom_option']:
                lt_realty_list = lt_realty_list.filter(bathroom='a')
            if '2' in bathroom_checkbox.cleaned_data['bathroom_option']:
                lt_realty_list = lt_realty_list.filter(bathroom='b')
            if '3' in bathroom_checkbox.cleaned_data['bathroom_option']:
                pass

        """ Фильтрация по мебели """

        furniture_checkbox = FurnitureFilterForm(request.POST)

        furniture__result_list = []
        if furniture_checkbox.is_valid():
            check_box_clean_data_list = list(map(int, furniture_checkbox.cleaned_data['furniture_option']))
            for furniture_realty_filter in lt_realty_list:
                lt_realty_furniture_list = [furniture.id for furniture in furniture_realty_filter.furniture.all()]
                if set(check_box_clean_data_list).issubset(lt_realty_furniture_list):
                    furniture__result_list.append(furniture_realty_filter.id)
            if len(check_box_clean_data_list) == 0:
                pass
            else:
                lt_realty_list = lt_realty_list.filter(id__in=furniture__result_list)

        """ Фильтрация по технике """

        technique_checkbox = TechniqueFilterForm(request.POST)

        technique__result_list = []
        if technique_checkbox.is_valid():
            check_box_clean_data_list = list(map(int, technique_checkbox.cleaned_data['technique_option']))
            for technique_realty_filter in lt_realty_list:
                lt_realty_technique_list = [technique.id for technique in technique_realty_filter.technique.all()]
                if set(check_box_clean_data_list).issubset(lt_realty_technique_list):
                    technique__result_list.append(technique_realty_filter.id)
            if len(check_box_clean_data_list) == 0:
                pass
            else:
                lt_realty_list = lt_realty_list.filter(id__in=technique__result_list)

        all_lt_realty = LongTermRentObject.objects.all()  # Список всех объектов недвижимости для работы с фильтрами
        adv_lt_realty_list = lt_realty_list.filter(is_advertised=True)

        return render(request, 'app_ltrent/lt_realty_list.html',
                      {
                          'lt_realty_list': lt_realty_list, 'price_filter': price_filter, 'main_filter': main_filter,
                          'adv_lt_realty_list': adv_lt_realty_list, 'area_filter': area_filter,
                          'floor_filter': floor_filter, 'rules_checkbox': rules_checkbox,
                          'bathroom_checkbox': bathroom_checkbox, 'furniture_checkbox': furniture_checkbox,
                          'technique_checkbox': technique_checkbox,
                      }
                      )

    lt_realty_list = LongTermRentObject.objects.prefetch_related('furniture').prefetch_related('technique')
    main_filter = DropdownFilterLongTermForm()
    price_filter = PriseFilterForm()
    area_filter = AreaFilterForm()
    floor_filter = AreaFilterForm()
    rules_checkbox = RulesFilterForm()
    bathroom_checkbox = BathroomFilterForm()
    furniture_checkbox = FurnitureFilterForm()
    technique_checkbox = TechniqueFilterForm()
    realty_type_checkbox = RealtyTypeCheckBoxForm()
    adv_lt_realty_list = lt_realty_list.filter(is_advertised=True)

    return render(request, 'app_ltrent/lt_realty_list.html',
                  {
                      'lt_realty_list': lt_realty_list,
                      'price_filter': price_filter,
                      'main_filter': main_filter,
                      'realty_type_checkbox': realty_type_checkbox,
                      'adv_lt_realty_list': adv_lt_realty_list,
                      'area_filter': area_filter,
                      'floor_filter': floor_filter,
                      'rules_checkbox': rules_checkbox,
                      'bathroom_checkbox': bathroom_checkbox,
                      'furniture_checkbox': furniture_checkbox,
                      'technique_checkbox': technique_checkbox,
                  }
                  )


"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""


class LongTermRealtyDetailView(generic.DetailView):
    """Детальная информация по каждому объекту"""
    model = LongTermRentObject
    template_name = 'app_ltrent/lt_realty_detail.html'
    context_object_name = 'lt_realty'
    queryset = LongTermRentObject.objects.prefetch_related('furniture').prefetch_related('technique')

    def get_success_url(self):
        return reverse('lt_detail_view', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LongTermRealtyDetailView, self).get_form_kwargs(
            *args, **kwargs
        )
        return kwargs

    def get_context_data(self, *args, **kwargs):
        """Передача дополнительных моделей в шаблон через контекст"""
        context = super(LongTermRealtyDetailView, self).get_context_data(**kwargs)
        pk = kwargs['object'].id
        current_user = self.request.user.id
        current_account = CustomUser.objects.get(id=current_user)
        current_realty = LongTermRentObject.objects.get(id=pk)
        current_company = CompanyProfile.objects.get(user=current_user)
        advertised_realty = LongTermRentObject.objects.filter(is_advertised=True)
        deposit_sum = current_realty.deposit * current_realty.realty_price

        """ Наборы данных для вывода в раздел 'так же у этой компании' в детальной информации объектов """

        adv_lt_realty = LongTermRentObject.objects.filter(company=current_company.id).exclude(id=pk)
        adv_hd_realty = HolidayHouseObject.objects.filter(company=current_company.id)
        context['adv_lt_realty'] = adv_lt_realty
        context['adv_hd_realty'] = adv_hd_realty

        context['current_realty'] = current_realty
        context['current_company'] = current_company
        context['advertised_realty'] = advertised_realty
        context['detail_photos'] = LongTermPhotos.objects.filter(long_term_obj=pk)
        context['deposit_sum'] = deposit_sum
        context['current_account'] = current_account

        return context

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and 'detail__send_feedback' in request.POST:
            slug = self.kwargs.get('slug')
            realty_id = LongTermRentObject.objects.get(slug=slug)
            comments_form = CommentsForm(request.POST)
            if comments_form.is_valid():
                comments_form.user_id = CustomUser.objects.get(id=request.user.id)
                comments_form.realty_id = realty_id.id
                comments_form.save()

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

        return redirect('app_premises:realty_detail', pk=self.kwargs.get('pk'))


class LonTermRealtyEditFromView(View):
    def get(self, request, pk):
        if 'delete_lt_photo_button' in request.GET:
            pk = request.GET.get('delete_photo_button').split(', ')[1]
            current_photo = LongTermPhotos.objects.get(id=pk)
            if os.path.isfile(f'media/{current_photo.photo}'):
                current_photo.delete()
                os.remove(f'media/{current_photo.photo}')
            return redirect('app_ltrent:lt_realty_edit', pk=self.kwargs.get('pk'))
        if request.user.is_authenticated and request.user.is_company:
            current_manager = CompanyProfile.objects.get(user=request.user.id)
            realty_edit = LongTermRentObject.objects.get(id=pk)

            if realty_edit.company == current_manager:
                realty_edit_form = LongTermRentObjectForm(instance=realty_edit)
                upload_photos_form = PhotosForm(request.FILES, initial={'realty_obj': realty_edit.id})
                return render(request, 'app_ltrent/lt_edit_realty.html',
                              context={'realty_edit_form': realty_edit_form, 'pk': pk, 'realty_edit': realty_edit,
                                       'upload_photos_form': upload_photos_form
                                       }
                              )
            else:
                retour = permission_denied(request)
                return HttpResponseForbidden(retour)

        else:
            return HttpResponseRedirect('/')

    def post(self, request, pk):
        if request.method == 'POST':
            realty_edit = LongTermRentObject.objects.get(id=pk)
            realty_edit_form = LongTermRentObjectForm(request.POST, instance=realty_edit)
            upload_photos_form = PhotosForm(request.POST, request.FILES, initial={'realty_obj': realty_edit.id})
            if realty_edit_form.is_valid():
                files = request.FILES.getlist('photo')
                realty_edit.save()
                for photo in files:
                    LongTermPhotos.objects.create(realty_obj=realty_edit, photo=photo)

            elif 'lt_realty_edit_submitting_photo' in request.POST:
                if upload_photos_form.is_valid():
                    files = request.FILES.getlist('photo')
                    for photo in files:
                        LongTermPhotos.objects.create(realty_obj=realty_edit, photo=photo)
                    return redirect('app_ltrent:lt_realty_edit', pk=pk)

                else:
                    return redirect('app_ltrent:lt_realty_edit', pk=pk)

            else:
                return redirect('app_ltrent:lt_realty_edit', pk=pk)

            return render(request, 'app_ltrent/lt_edit_realty.html',
                          context={'realty_edit_form': realty_edit_form, 'pk': pk, 'realty_edit': realty_edit,
                                   'upload_photos_form': upload_photos_form
                                   }
                          )


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""


# class ReservationFormView(View):
#
#     def get(self, request, *args, **kwargs):
#         if 'to-reserve-page' in request.GET:
#             if request.user.is_authenticated:
#                 realty = request.GET.get('to-reserve-page').split(', ')[0]
#                 current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
#                 current_user = CustomUser.objects.get(id=request.user.id)
#                 check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2],
#                                                       "%Y-%m-%d").date()
#                 check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3],
#                                                        "%Y-%m-%d").date()
#                 total_sum = (check_out - check_in).days * int(current_realty_price)
#                 reservation_form = ReservationForm(
#                     initial={'realty': realty, 'guest': current_user, 'check_in': check_in, 'check_out': check_out,
#                              'total_sum': total_sum, 'is_booked': False})
#                 realty_object_to_reserve_page = LongTermRentObject.objects.get(id=realty)
#                 photos = Photos.objects.filter(realty_obj=realty).first()
#                 reserve_register_form = RegisterForm()
#
#                 return render(request, 'app_premises/reservation.html',
#                               context={'reservation_form': reservation_form,
#                                        'realty_object_to_reserve_page': realty_object_to_reserve_page,
#                                        'current_user': current_user,
#                                        'check_in': check_in,
#                                        'check_out': check_out,
#                                        'total_sum': total_sum,
#                                        'photos': photos, 'reserve_register_form': reserve_register_form
#                                        }
#                               )
#
#             else:
#                 auth_form = AuthForm()
#                 realty = request.GET.get('to-reserve-page').split(', ')[0]
#                 current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
#                 check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2],
#                                                       "%Y-%m-%d").date()
#                 check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3],
#                                                        "%Y-%m-%d").date()
#                 total_sum = (check_out - check_in).days * int(current_realty_price)
#                 realty_object_to_reserve_page = LongTermRentObject.objects.get(id=realty)
#                 photos = Photos.objects.filter(realty_obj=realty).first()
#                 reservation_form = ReservationForm(initial={'realty': realty, 'check_in': check_in,
#                                                             'check_out': check_out, 'total_sum': total_sum,
#                                                             'is_booked': False})
#                 reserve_register_form = RegisterForm()
#
#                 return render(request, 'app_premises/reservation.html',
#                               context={
#                                   'realty_object_to_reserve_page': realty_object_to_reserve_page,
#                                   'check_in': check_in,
#                                   'check_out': check_out,
#                                   'total_sum': total_sum,
#                                   'photos': photos,
#                                   'reservation_form': reservation_form,
#                                   'reserve_register_form': reserve_register_form,
#                                   'auth_form': auth_form,
#                               }
#                               )
#
#     def post(self, request, *args, **kwargs):
#         if 'reservation-submit' in request.POST:
#             realty = request.GET.get('to-reserve-page').split(', ')[0]
#             current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
#             current_user = CustomUser.objects.get(id=request.user.id)
#             check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2], "%Y-%m-%d").date()
#             check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3], "%Y-%m-%d").date()
#             total_sum = (check_out - check_in).days * int(current_realty_price)
#             reservation_form = ReservationForm(request.POST,
#                                                initial={'realty': realty, 'guest': current_user, 'check_in': check_in,
#                                                         'check_out': check_out,
#                                                         'total_sum': total_sum, 'is_booked': False})
#
#             if reservation_form.is_valid():
#                 reservation = reservation_form.save(commit=False)
#                 reservation.guest = current_user
#                 reservation.realty = LongTermRentObject.objects.get(id=realty)
#                 reservation.is_booked = True
#                 reservation.save()
#             else:
#                 pass
#
#             return HttpResponseRedirect('/')
#
#         if 'reserve__submit_login_form' in request.POST:
#             realty = request.GET.get('to-reserve-page').split(', ')[0]
#             current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
#             check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2], "%Y-%m-%d").date()
#             check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3], "%Y-%m-%d").date()
#             total_sum = (check_out - check_in).days * int(current_realty_price)
#             realty_object_to_reserve_page = LongTermRentObject.objects.get(id=realty)
#             photos = Photos.objects.filter(realty_obj=realty).first()
#             auth_form = AuthForm(request.POST)
#             if auth_form.is_valid():
#                 email = auth_form.cleaned_data['email']
#                 password = auth_form.cleaned_data['password']
#                 user = authenticate(email=email, password=password)
#                 if user:
#                     if user.is_active:
#                         login(request, user)
#                     else:
#                         auth_form.add_error('__all__', 'Проверьте правильность введёных данных')
#
#                 current_user = CustomUser.objects.get(id=request.user.id)
#                 reservation_form = ReservationForm(initial={'realty': realty, 'guest': current_user,
#                                                             'check_in': check_in,
#                                                             'check_out': check_out,
#                                                             'total_sum': total_sum, 'is_booked': False})
#
#                 return render(request, 'app_premises/reservation.html',
#                               context={'reservation_form': reservation_form,
#                                        'realty_object_to_reserve_page': realty_object_to_reserve_page,
#                                        'check_in': check_in,
#                                        'check_out': check_out,
#                                        'total_sum': total_sum,
#                                        'photos': photos,
#                                        'current_user': current_user
#                                        }
#                               )
#
#         if 'reserve__register_form_submit' in request.POST:
#             reserve_register_form = RegisterForm(request.POST, initial={'phone': '+7'})
#             realty = request.GET.get('to-reserve-page').split(', ')[0]
#             current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
#             check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2],
#                                                   "%Y-%m-%d").date()
#             check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3],
#                                                    "%Y-%m-%d").date()
#             total_sum = (check_out - check_in).days * int(current_realty_price)
#             realty_object_to_reserve_page = LongTermRentObject.objects.get(id=realty)
#             photos = Photos.objects.filter(realty_obj=realty).first()
#             auth_form = AuthForm(request.POST)
#
#             if reserve_register_form.is_valid():
#                 user = reserve_register_form.save()
#                 last_name = reserve_register_form.cleaned_data.get('last_name')
#                 first_name = reserve_register_form.cleaned_data.get('first_name')
#                 phone = reserve_register_form.cleaned_data.get('phone')
#                 email = reserve_register_form.cleaned_data.get('email')
#                 raw_password = reserve_register_form.cleaned_data.get('password1')
#                 is_active = reserve_register_form.cleaned_data.get('is_active')
#                 is_company = reserve_register_form.cleaned_data.get('is_company')
#
#                 user = authenticate(email=email, password=raw_password)
#                 login(request, user)
#
#                 current_user = CustomUser.objects.get(id=request.user.id)
#                 reservation_form = ReservationForm(initial={'realty': realty, 'guest': current_user,
#                                                             'check_in': check_in,
#                                                             'check_out': check_out,
#                                                             'total_sum': total_sum, 'is_booked': False})
#
#                 return render(request, 'app_premises/reservation.html',
#                               context={'reservation_form': reservation_form,
#                                        'realty_object_to_reserve_page': realty_object_to_reserve_page,
#                                        'check_in': check_in,
#                                        'check_out': check_out,
#                                        'total_sum': total_sum,
#                                        'photos': photos,
#                                        'current_user': current_user
#                                        }
#                               )
#             else:
#                 return HttpResponseRedirect('/')
#
#         else:
#             return HttpResponseRedirect('/')
#
#
# def permission_denied(request):
#     return render(request, '403.html')
