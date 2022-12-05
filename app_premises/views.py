import datetime
import os

from django.contrib.auth import authenticate, login
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from .models import Camp, Reservation, Photos, Advertising
from .forms import ReservationForm, PriseFilterForm, DropdownFilterForm, RealtyTypeCheckBoxForm, \
    OptionFilterForm, InRoomOptionFilterForm, FoodOptionFilterForm, HolidayHouseForm, PhotosForm, BookCancelForm, \
    PayTypeForm, CreateHolidayHouseForm, FlatForm, DropdownFilterLongTermForm, \
    AreaFilterForm, BathroomFilterForm, RulesFilterForm, FurnitureFilterForm, TechniqueFilterForm, FloorFilterForm, \
    CreateHolidayHouseForm1, CreateHolidayHouseForm2, CreateHolidayHouseForm3, CreateHolidayHouseForm4, \
    CreateHolidayHouseForm5, CreateHolidayHouseForm6, CreateHolidayHouseForm7, ReservationListSearchForm

from app_profiler.models import CustomUser
from app_profiler.forms import RegisterForm, AuthForm
from app_comments.forms import CommentsForm
from app_comments.models import Comments
from app_premises.models import Favorite, Flat
from app_data.models import Ip
from app_data.views import get_client_ip


def main_realty_list(request):
    """
        Получаем параметры с index.html форм и по ним фильтруем поисковую выдачу:
        - Страна
        - Город
    """

    if 'search' in request.GET or 'realty_list__search' in request.POST:

        reservation_set = []
        list_reserve_form = ReservationListSearchForm()

        if request.GET.get('check_out') or request.POST.get('check_out'):
            """Помечаем забронированные объекты в искомые даты"""
            if request.method == 'GET':
                searched_check_in = datetime.datetime.strptime(request.GET.get('check_in'), "%d.%m.%Y").date()
                searched_check_out = datetime.datetime.strptime(request.GET.get('check_out'), "%d.%m.%Y").date()
            elif request.method == 'POST' and not 'submit-login-form' in request.POST:
                searched_check_in = datetime.datetime.strptime(request.POST.get('check_in'), "%d.%m.%Y").date()
                searched_check_out = datetime.datetime.strptime(request.POST.get('check_out'), "%d.%m.%Y").date()

            reservations_list = Reservation.objects.select_related('realty')

            if not 'submit-login-form' in request.POST:
                for reservation in reservations_list:
                    if reservation.is_booked:
                        if searched_check_out > reservation.check_in and searched_check_in < reservation.check_out \
                                or reservation.check_in < searched_check_out < reservation.check_out \
                                or reservation.check_in <= searched_check_in < reservation.check_out \
                                or searched_check_in == reservation.check_in and searched_check_out == reservation.check_out \
                                or searched_check_in <= reservation.check_in and searched_check_out >= reservation.check_out \
                                or searched_check_in < reservation.check_out < searched_check_out:
                            reservation_set.append(
                                {'obj_id': reservation.realty.id, 'obj_check_in': str(reservation.check_in),
                                 'obj_check_out': str(reservation.check_out)})

                list_reserve_form = ReservationListSearchForm(initial={
                    'check_in': searched_check_in,
                    'check_out': searched_check_out}
                )

            else:
                pass

        if request.GET.get('q') is None:
            query = request.POST.get('q')
        else:
            query = request.GET.get('q')

        searched_city = query

        realty_list = Camp.objects.filter(
            Q(realty_country__iregex=query) | Q(realty_city__iregex=query) | Q(realty_region__iregex=query))

        """ Фильтрация 'Сначала дорогое', ... """
        main_filter = DropdownFilterForm(request.POST)
        if main_filter.is_valid():
            if main_filter.cleaned_data['popular_first'] == 'i':
                realty_list = realty_list.order_by('realty_price')

            if main_filter.cleaned_data['popular_first'] == 'x':
                realty_list = realty_list.order_by('-realty_price')

            if main_filter.cleaned_data['popular_first'] == 'p':
                realty_list = realty_list.order_by('-realty_book_count')

        """ Фильтрация по диапазону цен """
        price_filter = PriseFilterForm(request.POST)
        if price_filter.is_valid():
            if price_filter.cleaned_data['min_price']:
                realty_list = realty_list.filter(realty_price__gte=price_filter.cleaned_data['min_price'])

            if price_filter.cleaned_data['max_price']:
                realty_list = realty_list.filter(realty_price__lte=price_filter.cleaned_data['max_price'])

        """ Фильтрация по типам помещений """
        realty_type_checkbox = RealtyTypeCheckBoxForm(request.POST)

        realty_type_index = ['h', 'c', 'a', 'ah', 'gh', 'k', 'v', 'kp', 'gp']
        type_result_list = []

        if realty_type_checkbox.is_valid():
            for _type in realty_type_index:
                if _type in realty_type_checkbox.cleaned_data['realty_type']:
                    type_result_list.append(_type)

            if len(realty_type_checkbox.cleaned_data['realty_type']) == 0:
                pass
            else:
                realty_list = realty_list.filter(realty_type__in=type_result_list)

        all_realty = Camp.objects.all()  # Список всех объектов недвижимости для работы с фильтрами

        """Фильтрация по опциям питания"""
        food_options_checkbox = FoodOptionFilterForm(request.POST)
        food_type_list = []

        if food_options_checkbox.is_valid():
            for realty in realty_list:
                if realty.food_options in food_options_checkbox.cleaned_data['option']:
                    food_type_list.append(realty.id)
            if len(food_options_checkbox.cleaned_data['option']) == 0:
                pass
            else:
                realty_list = realty_list.filter(id__in=food_type_list)

        """Фильтрация по отмене бронирования"""
        book_filter = BookCancelForm(request.POST)
        book_type_list = []

        if book_filter.is_valid():
            for realty in all_realty:
                if realty.book_cancel in book_filter.cleaned_data['cancel_type']:
                    book_type_list.append(realty.id)
            if len(book_filter.cleaned_data['cancel_type']) == 0:
                pass
            else:
                realty_list = realty_list.filter(id__in=book_type_list)

        """Фильтрация по типу оплаты"""
        pay_filter = PayTypeForm(request.POST)
        pay_type_list = []

        if pay_filter.is_valid():
            for realty in all_realty:
                if realty.pay_type in pay_filter.cleaned_data['pay_type']:
                    pay_type_list.append(realty.id)
            if len(pay_type_list) == 0:
                pass
            else:
                realty_list = realty_list.filter(id__in=pay_type_list)

        """Фильтрация по опциям в отеле и в номере"""

        hotel_filter_checkbox = OptionFilterForm(request.POST)

        in_hotel__result_list = []
        if hotel_filter_checkbox.is_valid():
            check_box_clean_data_list = list(map(int, hotel_filter_checkbox.cleaned_data['hotel_option']))
            for in_hotel_realty_filter in realty_list:
                realty_option_list = [option.id for option in in_hotel_realty_filter.options.all()]
                if set(check_box_clean_data_list).issubset(realty_option_list):
                    in_hotel__result_list.append(in_hotel_realty_filter.id)
            if len(check_box_clean_data_list) == 0:
                pass
            else:
                realty_list = realty_list.filter(id__in=in_hotel__result_list)

        room_filter_checkbox = InRoomOptionFilterForm(request.POST)

        in_room__result_list = []
        if room_filter_checkbox.is_valid():
            check_box_clean_data_list = list(map(int, room_filter_checkbox.cleaned_data['room_option']))
            for in_room_realty_filter in realty_list:
                realty_option_list = [option.id for option in in_room_realty_filter.options.all()]
                if set(check_box_clean_data_list).issubset(realty_option_list):
                    in_room__result_list.append(in_room_realty_filter.id)
            if len(check_box_clean_data_list) == 0:
                pass
            else:
                realty_list = realty_list.filter(id__in=in_room__result_list)

        favorite_list = Favorite.objects.none()
        if request.user.is_authenticated:
            favorite_list = Favorite.objects.filter(user=request.user.id).prefetch_related('camps', 'flats')

        adv_realty_list = realty_list.filter(is_advertised=True).select_related('company')
        adv1 = Advertising.objects.all()

        return render(request, 'app_premises/realty_list.html',
                      {
                          'realty_list': realty_list,
                          'price_filter': price_filter,
                          'main_filter': main_filter,
                          'realty_type_checkbox': realty_type_checkbox,
                          'hotel_filter_checkbox': hotel_filter_checkbox,
                          'reservation_set': reservation_set,
                          'list_reserve_form': list_reserve_form,
                          'room_filter_checkbox': room_filter_checkbox,
                          'food_options_checkbox': food_options_checkbox,
                          'book_filter': book_filter,
                          'pay_filter': pay_filter,
                          'adv_realty_list': adv_realty_list,
                          'searched_city': searched_city,
                          'favorite_list': favorite_list, 'adv1': adv1,
                      }
                      )
    else:
        realty_list = Camp.objects.select_related('company')
        list_reserve_form = ReservationListSearchForm()
        reservation_set = []
        room_filter_checkbox = InRoomOptionFilterForm()
        hotel_filter_checkbox = OptionFilterForm()
        pay_filter = PayTypeForm()
        book_filter = BookCancelForm()
        food_options_checkbox = FoodOptionFilterForm()
        realty_type_checkbox = RealtyTypeCheckBoxForm()
        price_filter = PriseFilterForm()
        main_filter = DropdownFilterForm()
        adv_realty_list = realty_list.filter(is_advertised=True)
        favorite_list = Favorite.objects.none()
        adv1 = Advertising.objects.all()
        if request.user.is_authenticated:
            favorite_list = Favorite.objects.filter(user=request.user.id).prefetch_related('camps', 'flats')

        return render(request, 'app_premises/realty_list.html',
                      {
                          'realty_list': realty_list,
                          'price_filter': price_filter,
                          'main_filter': main_filter,
                          'realty_type_checkbox': realty_type_checkbox,
                          'hotel_filter_checkbox': hotel_filter_checkbox,
                          'reservation_set': reservation_set,
                          'list_reserve_form': list_reserve_form,
                          'room_filter_checkbox': room_filter_checkbox,
                          'food_options_checkbox': food_options_checkbox,
                          'book_filter': book_filter,
                          'pay_filter': pay_filter,
                          'adv_realty_list': adv_realty_list,
                          'favorite_list': favorite_list, 'adv1': adv1,
                      }
                      )


""" РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ """


class RealtyDetailView(generic.DetailView):
    """Детальная информация по каждому объекту"""
    model = Camp
    template_name = 'realty_detail.html'
    context_object_name = 'realty'
    queryset = Camp.objects.prefetch_related('options')

    def get_success_url(self):
        return reverse('detail_view', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RealtyDetailView, self).get_form_kwargs(
            *args, **kwargs
        )
        return kwargs

    def check_is_permission_to_comment(self, user, realty):
        """
            При переходе на детальную страницу объекта мы проверяем есть ли в списке бронирований пользователя
            данный объект со статусами "не отменен" и "не активен" так как именно в этом случае наивысшая вероятность, что
            пользователь бронировал, не отменял и был в данном месте
        """
        today = datetime.datetime.now().date()
        reserves_of_current_user = Reservation.objects.filter(
            guest=user,
            realty=realty,
            is_booked=False,
            is_canceled=False,
            check_out__lte=today
        )

        if reserves_of_current_user:
            return True
        else:
            return False

    def get_context_data(self, *args, **kwargs):
        """ Передача дополнительных моделей в шаблон через контекст """
        context = super(RealtyDetailView, self).get_context_data(**kwargs)
        pk = kwargs['object'].id
        current_realty = Camp.objects.get(id=pk)
        current_company = CustomUser.objects.none()

        """ Объекты для раздела 'так же у этой компании' """
        adv_realty_list_curr_company = Camp.objects.filter(company=current_realty.company.id).exclude(
            id=pk)
        adv_lt_realty = Flat.objects.filter(company=current_realty.company.id)
        context['adv_lt_realty'] = adv_lt_realty
        context['adv_realty_list_curr_company'] = adv_realty_list_curr_company

        """ Получаем IP пользователя, проверяем в БД и добавляем в просмотры, если ещё не смотрел """
        ip = get_client_ip(self.request)
        if Ip.objects.filter(ip=ip).exists():
            current_realty.views_count.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            current_realty.views_count.add(Ip.objects.get(ip=ip))

        """ Заглушка текущего пользователя, если не авторизован """
        # TODO Проверить вариант CustomUser.objects.get(id=current_user, None)
        current_account = CustomUser.objects.none()

        if self.request.user.is_authenticated:
            current_user = self.request.user.id
            current_account = CustomUser.objects.get(id=current_user)
            if self.request.user.is_company:
                current_company = CustomUser.objects.get(id=current_user)

        realty_slug = current_realty.slug
        advertised_realty = Camp.objects.filter(is_advertised=True)

        """ Получаем данные для последующей передачи суммы бронирования """
        if 'check-is-reserve-available' in self.request.GET:
            current_realty_price = self.request.GET.get('check-is-reserve-available').split(', ')[1]
            check_in = datetime.datetime.strptime(self.request.GET.get('check_in'), "%d.%m.%Y").date()
            check_out = datetime.datetime.strptime(self.request.GET.get('check_out'), "%d.%m.%Y").date()
            total_sum = (check_out - check_in).days * int(current_realty_price)
            reservation_days_count = (check_out - check_in).days
            if self.request.user.is_authenticated:
                context['detail_reserve_form'] = ReservationForm(
                    initial={
                        'realty': pk,
                        'guest': self.request.user.id,
                        'check_in': check_in,
                        'check_out': check_out,
                    }
                )
            else:
                context['detail_reserve_form'] = ReservationForm(initial={'check_in': check_in, 'check_out': check_out})

            context['total_sum'] = total_sum
            context['reservation_days_count'] = reservation_days_count
        else:
            context['detail_reserve_form'] = ReservationForm()

        """ Получаем список опций конкретного отеля с категорией "В отеле" """
        realty_in_hotel_options_name = [option.option_name for option in
                                        current_realty.options.filter(category='В отеле')]
        realty_in_hotel_options_category = [option.category for option in
                                            current_realty.options.filter(category='В отеле')]
        realty_options_list_in_hotel = list(zip(realty_in_hotel_options_category, realty_in_hotel_options_name))
        context['hotel_options'] = realty_options_list_in_hotel

        context['realty_slug'] = realty_slug
        context['current_realty'] = current_realty
        context['current_company'] = current_company
        context['advertised_realty'] = advertised_realty
        context['current_account'] = current_account

        """ Получаем список опций конкретного отеля с категорией "В номере" """
        realty_in_room_options_name = [option.option_name for option in
                                       current_realty.options.filter(category='В номере')]
        realty_in_room_options_category = [option.category for option in
                                           current_realty.options.filter(category='В номере')]
        realty_options_list_in_room = list(zip(realty_in_room_options_category, realty_in_room_options_name))
        context['room_options'] = realty_options_list_in_room

        context['detail_photos'] = Photos.objects.filter(camp=pk)
        if self.request.user.is_authenticated:
            current_user = self.request.user.id

            if self.check_is_permission_to_comment(current_account, current_realty) or current_realty in \
                    Camp.objects.filter(company=self.request.user.id):
                context['comment_form'] = CommentsForm(
                    initial={
                        'user': current_user,
                        'realty': pk,
                    }
                )

        context['comments'] = Comments.objects.filter(realty=pk).order_by('-publish_at')
        context['comments_count'] = Comments.objects.annotate(Count('id')).filter(realty=pk)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and 'detail__send_feedback' in request.POST:
            slug = self.kwargs.get('slug')
            realty_id = Camp.objects.get(slug=slug)
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

        return redirect('app_premises:realty_detail', slug=self.kwargs.get('slug'))


class RealtyEditFromView(View):
    def get(self, request, slug):
        if 'delete_photo_button' in request.GET:
            pk = request.GET.get('delete_photo_button').split(', ')[1]
            current_photo = Photos.objects.get(id=pk)
            if os.path.isfile(f'media/{current_photo.photo}'):
                current_photo.delete()
                os.remove(f'media/{current_photo.photo}')
            return redirect('app_premises:realty_edit', slug=self.kwargs.get('slug'))
        if request.user.is_authenticated and request.user.is_company:
            current_manager = CustomUser.objects.get(id=request.user.id)
            realty_edit = Camp.objects.get(slug=slug)

            if realty_edit.company == current_manager:
                realty_edit_form = HolidayHouseForm(instance=realty_edit)
                upload_photos_form = PhotosForm(request.FILES, initial={'camp': realty_edit.id})
                return render(request, 'app_premises/edit_realty.html',
                              context={'realty_edit_form': realty_edit_form, 'slug': slug, 'realty_edit': realty_edit,
                                       'upload_photos_form': upload_photos_form
                                       }
                              )
            else:
                retour = permission_denied(request)
                return HttpResponseForbidden(retour)

        else:
            return HttpResponseRedirect('/')

    def post(self, request, slug):
        if request.method == 'POST':
            realty_edit = Camp.objects.get(slug=slug)
            realty_edit_form = HolidayHouseForm(request.POST, instance=realty_edit)
            upload_photos_form = PhotosForm(request.POST, request.FILES, initial={'camp': realty_edit.id})
            if realty_edit_form.is_valid():
                realty_edit_form.save(commit=False)
                files = request.FILES.getlist('photo')
                for photo in files:
                    Photos.objects.create(camp=realty_edit, photo=photo)

                if 'realty_edit_submitting_options' in request.POST:
                    realty_edit.options.clear()
                    options_list = realty_edit_form.cleaned_data['options']
                    realty_edit.options.add(*options_list)
                realty_edit.save()

            elif 'realty_edit_submitting_photo' in request.POST:
                if upload_photos_form.is_valid():
                    files = request.FILES.getlist('photo')
                    for photo in files:
                        Photos.objects.create(camp=realty_edit, photo=photo)
                    return redirect('app_premises:realty_edit', slug=slug)

                else:
                    return redirect('app_premises:realty_edit', slug=slug)

            else:
                return redirect('app_premises:realty_edit', slug=slug)

            return render(request, 'app_premises/edit_realty.html',
                          context={'realty_edit_form': realty_edit_form, 'slug': slug, 'realty_edit': realty_edit,
                                   'upload_photos_form': upload_photos_form
                                   }
                          )


def create_camp_object_step1(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Первый шаг - название объекта
    """

    hh_realty_form1 = CreateHolidayHouseForm1(initial={'company': request.user.id})

    if 'detail__change_button' in request.GET:
        current_object = Camp.objects.get(id=request.GET.get('detail__change_button'))
        hh_realty_form1 = CreateHolidayHouseForm1(instance=current_object)
        return render(request, 'app_premises/create_realty.html', context={'hh_realty_form1': hh_realty_form1})

    if request.method == "GET" and not 'detail__change_button' in request.GET:
        return render(request, 'app_premises/create_realty.html', context={'hh_realty_form1': hh_realty_form1})

    if request.method == "POST":
        hh_realty_form1 = CreateHolidayHouseForm1(request.POST, initial={'company': request.user.id})
        if hh_realty_form1.is_valid():
            current_object = hh_realty_form1.save(commit=False)
            current_object.company = CustomUser.objects.get(id=request.user.id)
            current_object.save()
            return redirect('app_premises:create_camp2')
        return render(request, 'app_premises/create_realty.html', context={'hh_realty_form1': hh_realty_form1})
    return render(request, 'app_premises/create_realty.html', context={'hh_realty_form1': hh_realty_form1})


def create_camp_object_step2(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Второй шаг - адрес
    """

    current_object = Camp.objects.filter(company=request.user.id).last()
    camp_object_form2 = CreateHolidayHouseForm2()
    if request.method == "POST":
        camp_object_form2 = CreateHolidayHouseForm2(request.POST)
        if camp_object_form2.is_valid():
            current_object.ind = camp_object_form2.cleaned_data['ind']
            current_object.realty_country = camp_object_form2.cleaned_data['realty_country']
            current_object.realty_city = camp_object_form2.cleaned_data['realty_city']
            current_object.realty_address = camp_object_form2.cleaned_data['realty_address']
            current_object.save()
            return redirect('app_premises:create_camp3')
        return redirect('app_premises:create_camp2')
    return render(request, 'app_premises/create_camp_step2.html',
                  context={'camp_object_form2': camp_object_form2, 'current_object': current_object})


def create_camp_object_step3(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Третий шаг - параметры объекта
    """

    current_object = Camp.objects.filter(company=request.user.id).last()
    camp_object_form3 = CreateHolidayHouseForm3()
    if request.method == "POST":
        camp_object_form3 = CreateHolidayHouseForm3(request.POST)
        if camp_object_form3.is_valid():
            current_object.stars = camp_object_form3.cleaned_data['stars']
            current_object.count_of_persons = camp_object_form3.cleaned_data['count_of_persons']
            current_object.realty_area = camp_object_form3.cleaned_data['realty_area']
            current_object.book_cancel = camp_object_form3.cleaned_data['book_cancel']
            current_object.pay_type = camp_object_form3.cleaned_data['pay_type']
            current_object.realty_type = camp_object_form3.cleaned_data['realty_type']
            current_object.food_options = camp_object_form3.cleaned_data['food_options']
            current_object.save()
            return redirect('app_premises:create_camp4')
        return redirect('app_premises:create_camp3')
    return render(request, 'app_premises/create_camp_step3.html', context={'camp_object_form3': camp_object_form3})


def create_camp_object_step4(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Четвертый шаг - опции
    """

    current_object = Camp.objects.filter(company=request.user.id).last()
    camp_object_form4 = CreateHolidayHouseForm4()
    if request.method == "POST":
        camp_object_form4 = CreateHolidayHouseForm4(request.POST)
        if camp_object_form4.is_valid():
            current_object.options.clear()
            options_list = camp_object_form4.cleaned_data['options']
            current_object.options.add(*options_list)
            return redirect('app_premises:create_camp5')
        return redirect('app_premises:create_camp4')
    return render(request, 'app_premises/create_camp_step4.html', context={'camp_object_form4': camp_object_form4})


def create_camp_object_step5(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Пятый шаг - условия проживания
    """

    current_object = Camp.objects.filter(company=request.user.id).last()
    camp_object_form5 = CreateHolidayHouseForm5()
    if request.method == "POST":
        camp_object_form5 = CreateHolidayHouseForm5(request.POST)
        if camp_object_form5.is_valid():
            current_object.arriving_time = camp_object_form5.cleaned_data['arriving_time']
            current_object.departure_time = camp_object_form5.cleaned_data['departure_time']
            current_object.save()
            return redirect('app_premises:create_camp6')
        return redirect('app_premises:create_camp5')
    return render(request, 'app_premises/create_camp_step5.html', context={'camp_object_form5': camp_object_form5})


def create_camp_object_step6(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Шестой шаг - фотографии
    """

    current_object = Camp.objects.filter(company=request.user.id).last()
    camp_object_form6 = PhotosForm()
    if request.method == "POST":
        camp_object_form6 = PhotosForm(request.POST, request.FILES, initial={'camp': current_object})
        if camp_object_form6.is_valid():
            files = request.FILES.getlist('photo')
            for photo in files:
                Photos.objects.create(camp=current_object, photo=photo)
            return redirect('app_premises:create_camp7')
        return redirect('app_premises:create_camp6')
    return render(request, 'app_premises/create_camp_step6.html', context={'camp_object_form6': camp_object_form6})


def create_camp_object_step7(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Седьмой шаг - описание
    """

    current_object = Camp.objects.filter(company=request.user.id).last()
    camp_object_form7 = CreateHolidayHouseForm6()
    if request.method == "POST":
        camp_object_form7 = CreateHolidayHouseForm6(request.POST, request.FILES, initial={'realty_obj': current_object})
        if camp_object_form7.is_valid():
            current_object.full_description = camp_object_form7.cleaned_data['full_description']
            current_object.save()
            return redirect('app_premises:create_camp8')
        return redirect('app_premises:create_camp7')
    return render(request, 'app_premises/create_camp_step7.html', context={'camp_object_form7': camp_object_form7})


def create_camp_object_step8(request):
    """
    Представление для создания объекта в категории Альтернативные варианты размещения. Восьмой шаг - цена
    """

    current_object = Camp.objects.filter(company=request.user.id).last()
    camp_object_form8 = CreateHolidayHouseForm7()
    if request.method == "POST":
        camp_object_form8 = CreateHolidayHouseForm7(request.POST)
        if camp_object_form8.is_valid():
            current_object.realty_price = camp_object_form8.cleaned_data['realty_price']
            current_object.save()
            return redirect('app_premises:realty_detail', slug=current_object.slug)
        return redirect('app_premises:create_camp8')
    return render(request, 'app_premises/create_camp_step8.html', context={'camp_object_form8': camp_object_form8})


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""


class ReservationFormView(View):
    def get(self, request, *args, **kwargs):
        if 'to-reserve-page' in request.GET:
            if request.user.is_authenticated:
                """ Получаем данные из GET запроса и передаём их в форму, чтобы пользователь не вводил повторно """
                realty = request.GET.get('to-reserve-page').split(', ')[0]
                current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
                check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2],
                                                      "%Y-%m-%d").date()
                check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3],
                                                       "%Y-%m-%d").date()
                total_sum = (check_out - check_in).days * int(current_realty_price)

                realty_object_to_reserve_page = Camp.objects.get(id=realty)
                photos = Photos.objects.filter(camp=realty).first()
                reserve_register_form = RegisterForm()

                if self.request.user.is_authenticated:
                    current_user = CustomUser.objects.get(id=request.user.id)
                    reservation_form = ReservationForm(
                        initial={'realty': realty, 'guest': current_user, 'check_in': check_in, 'check_out': check_out,
                                 'total_sum': total_sum, 'is_booked': False})
                else:
                    reservation_form = ReservationForm()
                    current_user = None

                return render(request, 'app_premises/reservation.html',
                              context={'reservation_form': reservation_form,
                                       'realty_object_to_reserve_page': realty_object_to_reserve_page,
                                       'current_user': current_user,
                                       'check_in': check_in,
                                       'check_out': check_out,
                                       'total_sum': total_sum,
                                       'photos': photos, 'reserve_register_form': reserve_register_form
                                       }
                              )

            else:
                auth_form = AuthForm()
                realty = request.GET.get('to-reserve-page').split(', ')[0]
                current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
                check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2],
                                                      "%Y-%m-%d").date()
                check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3],
                                                       "%Y-%m-%d").date()
                total_sum = (check_out - check_in).days * int(current_realty_price)
                realty_object_to_reserve_page = Camp.objects.get(id=realty)
                photos = Photos.objects.filter(camp=realty).first()
                reservation_form = ReservationForm(initial={'realty': realty, 'check_in': check_in,
                                                            'check_out': check_out, 'total_sum': total_sum,
                                                            'is_booked': False})
                reserve_register_form = RegisterForm()

                return render(request, 'app_premises/reservation.html',
                              context={
                                  'realty_object_to_reserve_page': realty_object_to_reserve_page,
                                  'check_in': check_in,
                                  'check_out': check_out,
                                  'total_sum': total_sum,
                                  'photos': photos,
                                  'reservation_form': reservation_form,
                                  'reserve_register_form': reserve_register_form,
                                  'auth_form': auth_form,
                              }
                              )

    def post(self, request, *args, **kwargs):
        if 'reservation-submit' in request.POST:
            realty = request.GET.get('to-reserve-page').split(', ')[0]
            current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
            # TODO попробовать get(id=..., None) конструкцию
            current_user = CustomUser.objects.none()
            if self.request.user.is_authenticated:
                current_user = CustomUser.objects.get(id=request.user.id)
            check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2], "%Y-%m-%d").date()
            check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3], "%Y-%m-%d").date()
            total_sum = (check_out - check_in).days * int(current_realty_price)
            reservation_form = ReservationForm(request.POST,
                                               initial={'realty': realty, 'guest': current_user, 'check_in': check_in,
                                                        'check_out': check_out,
                                                        'total_sum': total_sum, 'is_booked': False})

            if reservation_form.is_valid():
                reservation = reservation_form.save(commit=False)
                reserved_realty = Camp.objects.get(id=int(realty))
                reserved_realty.realty_book_count += 1
                reserved_realty.save()
                reservation.guest = current_user
                reservation.realty = Camp.objects.get(id=realty)
                reservation.is_booked = True
                reservation.save()
            else:
                pass

            return HttpResponseRedirect('/')

        if 'submit-login-form' in request.POST:
            realty = request.GET.get('to-reserve-page').split(', ')[0]
            current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
            check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2], "%Y-%m-%d").date()
            check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3], "%Y-%m-%d").date()
            total_sum = (check_out - check_in).days * int(current_realty_price)
            realty_object_to_reserve_page = Camp.objects.get(id=realty)
            photos = Photos.objects.filter(camp=realty).first()
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

                current_user = CustomUser.objects.get(id=request.user.id)
                reservation_form = ReservationForm(initial={'realty': realty, 'guest': current_user,
                                                            'check_in': check_in,
                                                            'check_out': check_out,
                                                            'total_sum': total_sum, 'is_booked': False})

                return render(request, 'app_premises/reservation.html',
                              context={'reservation_form': reservation_form,
                                       'realty_object_to_reserve_page': realty_object_to_reserve_page,
                                       'check_in': check_in,
                                       'check_out': check_out,
                                       'total_sum': total_sum,
                                       'photos': photos,
                                       'current_user': current_user
                                       }
                              )

        if 'reserve__register_form_submit' in request.POST:
            reserve_register_form = RegisterForm(request.POST, initial={'phone': '+7'})
            realty = request.GET.get('to-reserve-page').split(', ')[0]
            current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
            check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2],
                                                  "%Y-%m-%d").date()
            check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3],
                                                   "%Y-%m-%d").date()
            total_sum = (check_out - check_in).days * int(current_realty_price)
            realty_object_to_reserve_page = Camp.objects.get(id=realty)
            photos = Photos.objects.filter(camp=realty).first()
            auth_form = AuthForm(request.POST)

            if reserve_register_form.is_valid():
                user = reserve_register_form.save()
                last_name = reserve_register_form.cleaned_data.get('last_name')
                first_name = reserve_register_form.cleaned_data.get('first_name')
                phone = reserve_register_form.cleaned_data.get('phone')
                email = reserve_register_form.cleaned_data.get('email')
                raw_password = reserve_register_form.cleaned_data.get('password1')
                is_active = reserve_register_form.cleaned_data.get('is_active')
                is_company = reserve_register_form.cleaned_data.get('is_company')

                user = authenticate(email=email, password=raw_password)
                login(request, user)

                current_user = CustomUser.objects.get(id=request.user.id)
                reservation_form = ReservationForm(initial={'realty': realty, 'guest': current_user,
                                                            'check_in': check_in,
                                                            'check_out': check_out,
                                                            'total_sum': total_sum, 'is_booked': False})

                return render(request, 'app_premises/reservation.html',
                              context={'reservation_form': reservation_form,
                                       'realty_object_to_reserve_page': realty_object_to_reserve_page,
                                       'check_in': check_in,
                                       'check_out': check_out,
                                       'total_sum': total_sum,
                                       'photos': photos,
                                       'current_user': current_user
                                       }
                              )
            else:
                return HttpResponseRedirect('/')

        else:
            return HttpResponseRedirect('/')


class HolidayHouseObjectFormView(View):

    def get(self, request):
        current_company = CustomUser.objects.get(id=request.user.id)
        hh_realty_form1 = CreateHolidayHouseForm1(initial={'company': current_company})
        upload_photos_form = PhotosForm(request.FILES)
        return render(request, 'app_premises/create_realty.html',
                      context={'hh_realty_form1': hh_realty_form1, 'upload_photos_form': upload_photos_form})

    def post(self, request):
        context = {}
        current_company = CustomUser.objects.get(id=request.user.id)

        if 'realty_create__save_realty_object' in request.POST:
            hh_realty_form = CreateHolidayHouseForm(request.POST, request.FILES)
            upload_photos_form = PhotosForm(request.FILES)
            if hh_realty_form.is_valid() and upload_photos_form.is_valid():
                hh_realty = hh_realty_form.save(commit=False)
                files = request.FILES.getlist('photo')
                hh_realty.save()
                for photo in files:
                    Photos.objects.create(camp=hh_realty, photo=photo)
            return redirect('app_profiler:company_detail', slug=current_company.slug)
        else:
            hh_realty_form = CreateHolidayHouseForm()
        context['form'] = hh_realty_form
        return render(request, 'app_premises/create_realty.html', context={'hh_realty_form': hh_realty_form})


def permission_denied(request):
    """ Страница permission denied """

    return render(request, '403.html')


def favorite(request):
    """ AJAX функция для добавления в избранное или удаление из избранного """

    realty_id = request.GET.get('realty_id', None)
    current_hh = Camp.objects.get(id=realty_id)
    favorite_list = Favorite.objects.filter(user=request.user.id).first()
    if not current_hh in favorite_list.camps.all():
        Favorite.objects.get(user=request.user.id).camps.add(Camp.objects.get(id=realty_id))
        return HttpResponse('to', content_type='text/html')
    else:
        Favorite.objects.get(user=request.user.id).camps.remove(Camp.objects.get(id=realty_id))
        return HttpResponse('from', content_type='text/html')


def add_comment(request):
    """ AJAX функция для отправки отзывов на объекты размещения """

    user = CustomUser.objects.get(id=request.GET.get('user'))
    realty = Camp.objects.get(id=request.GET.get('realty'))
    comment_text = request.GET.get('comment_text')
    data = Comments.objects.create(user=user, realty=realty, comment_text=comment_text)
    return HttpResponse(data, content_type='text/html')


# def create_camp_object(request):
#     user = CustomUser.objects.get(id=request.user.id)
#     current_object = HolidayHouseObject.objects.create(company=user, realty_name=request.GET.get('name'))
#     camp_form_step2 = CreateHolidayHouseForm2(instance=current_object)
#     return HttpResponse(camp_form_step2, content_type='text/html')


""" Представления объектов недвижимости на долгий срок """


def main_lt_realty_list(request):
    """
        Получаем параметры с index.html форм и по ним фильтруем поисковую выдачу:
        - Страна
        - Город
    """

    if 'lt_realty_list__search' in request.POST:
        query = request.POST.get('lt')

        searched_city = query

        lt_realty_list = Flat.objects.filter(
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

        all_lt_realty = Flat.objects.all()  # Список всех объектов недвижимости для работы с фильтрами
        adv_lt_realty_list = lt_realty_list.filter(is_advertised=True)

        """ Проверяем залогинен пользователь или нет, если да , то берём его список избранного и передаём в шаблон """
        favorite_list = Favorite.objects.none()
        if request.user.is_authenticated:
            favorite_list = Favorite.objects.filter(user=request.user.id).prefetch_related('camps', 'flats')

        return render(request, 'app_premises/lt_realty_list.html',
                      {
                          'lt_realty_list': lt_realty_list, 'price_filter': price_filter, 'main_filter': main_filter,
                          'adv_lt_realty_list': adv_lt_realty_list, 'area_filter': area_filter,
                          'floor_filter': floor_filter, 'rules_checkbox': rules_checkbox,
                          'bathroom_checkbox': bathroom_checkbox, 'furniture_checkbox': furniture_checkbox,
                          'technique_checkbox': technique_checkbox, 'searched_city': searched_city,
                          'favorite_list': favorite_list,
                      }
                      )

    lt_realty_list = Flat.objects.prefetch_related('furniture').prefetch_related('technique')
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

    """ Проверяем залогинен пользователь или нет, если да , то берём его список избранного и передаём в шаблон """
    favorite_list = Favorite.objects.none()
    if request.user.is_authenticated:
        favorite_list = Favorite.objects.filter(user=request.user.id).prefetch_related('camps', 'flats')

    return render(request, 'app_premises/lt_realty_list.html',
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
                      'favorite_list': favorite_list}
                  )


"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""


class LongTermRealtyDetailView(generic.DetailView):
    """Детальная информация по каждому объекту"""
    model = Flat
    template_name = 'app_premises/lt_realty_detail.html'
    context_object_name = 'lt_realty'
    queryset = Flat.objects.prefetch_related('furniture').prefetch_related('technique')

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
        current_realty = Flat.objects.get(id=pk)
        advertised_realty = Flat.objects.filter(is_advertised=True)
        current_company = current_realty.company
        current_account = CustomUser.objects.none()

        """ Получаем IP адреса пользователей и уникальные пишем в БД """
        ip = get_client_ip(self.request)

        if Ip.objects.filter(ip=ip).exists():
            current_realty.views_count.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            current_realty.views_count.add(Ip.objects.get(ip=ip))

        if self.request.user.is_authenticated:
            current_user = self.request.user.id
            current_account = CustomUser.objects.get(id=current_user)

        """ Наборы данных для вывода в раздел 'так же у этой компании' в детальной информации объектов """

        adv_lt_realty = Flat.objects.filter(company=current_company.id).exclude(id=pk)
        adv_hd_realty = Camp.objects.filter(company=current_company.id)
        context['adv_lt_realty'] = adv_lt_realty
        context['adv_hd_realty'] = adv_hd_realty

        context['current_realty'] = current_realty
        context['current_company'] = current_company
        context['advertised_realty'] = advertised_realty
        context['detail_photos'] = Photos.objects.filter(long_term_obj=pk)
        context['current_account'] = current_account

        return context

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and 'detail__send_feedback' in request.POST:
            slug = self.kwargs.get('slug')
            realty_id = Flat.objects.get(slug=slug)
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
            current_photo = Photos.objects.get(id=pk)
            if os.path.isfile(f'media/{current_photo.photo}'):
                current_photo.delete()
                os.remove(f'media/{current_photo.photo}')
            return redirect('app_premises:lt_realty_edit', pk=self.kwargs.get('pk'))
        if request.user.is_authenticated and request.user.is_company:
            current_manager = CustomUser.objects.get(id=request.user.id)
            realty_edit = Flat.objects.get(id=pk)

            if realty_edit.company == current_manager:
                realty_edit_form = FlatForm(instance=realty_edit)
                upload_photos_form = FlatForm(request.FILES, initial={'flat': realty_edit.id})
                return render(request, 'app_premises/lt_edit_realty.html',
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
            realty_edit = Flat.objects.get(id=pk)
            realty_edit_form = FlatForm(request.POST, instance=realty_edit)
            upload_photos_form = PhotosForm(request.POST, request.FILES, initial={'flat': realty_edit.id})
            if realty_edit_form.is_valid():
                realty_edit_form.save(commit=False)
                if 'realty_edit_submitting_technique' in request.POST:
                    realty_edit.technique.clear()
                    technique_list = realty_edit_form.cleaned_data['technique']
                    realty_edit.technique.add(*technique_list)

                if 'realty_edit_submitting_furniture' in request.POST:
                    realty_edit.furniture.clear()
                    furniture_list = realty_edit_form.cleaned_data['furniture']
                    realty_edit.furniture.add(*furniture_list)

                files = request.FILES.getlist('photo')
                realty_edit.save()
                for photo in files:
                    Photos.objects.create(long_term_obj=realty_edit, photo=photo)

            elif 'lt_realty_edit_submitting_photo' in request.POST:
                if upload_photos_form.is_valid():
                    files = request.FILES.getlist('photo')
                    for photo in files:
                        Photos.objects.create(long_term_obj=realty_edit, photo=photo)
                    return redirect('app_premises:lt_realty_edit', pk=pk)

                else:
                    return redirect('app_premises:lt_realty_edit', pk=pk)

            else:
                return redirect('app_premises:lt_realty_edit', pk=pk)

            return render(request, 'app_premises/lt_edit_realty.html',
                          context={'realty_edit_form': realty_edit_form, 'pk': pk, 'realty_edit': realty_edit,
                                   'upload_photos_form': upload_photos_form
                                   }
                          )


class LongTermObjectFormView(View):

    def get(self, request):
        current_company = CustomUser.objects.get(id=request.user.id)
        lt_realty_form = FlatForm(initial={'company': current_company})
        upload_photos_form = PhotosForm(request.FILES)
        return render(request, 'app_premises/lt_create_realty.html',
                      context={'lt_realty_form': lt_realty_form, 'upload_photos_form': upload_photos_form})

    def post(self, request):
        context = {}
        current_company = CustomUser.objects.get(id=request.user.id)
        if 'lt_realty_create__save_realty_object' in request.POST:
            lt_realty_form = FlatForm(request.POST, request.FILES)
            upload_photos_form = PhotosForm(request.FILES)
            if lt_realty_form.is_valid() and upload_photos_form.is_valid():
                lt_realty = lt_realty_form.save(commit=False)
                files = request.FILES.getlist('photo')
                lt_realty.save()
                for photo in files:
                    Photos.objects.create(long_term_obj=lt_realty, photo=photo)
            return redirect('app_companies:company_detail', company_slug=current_company.slug)
        else:
            lt_realty_form = FlatForm()
        context['form'] = lt_realty_form
        return render(request, 'app_premises/lt_create_realty.html', context={'lt_realty_form': lt_realty_form})


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""


def lt_favorite(request):
    realty_id = request.GET.get('realty_id', None)
    current_lt = Flat.objects.get(id=realty_id)
    favorite_list = Favorite.objects.filter(user=request.user.id).first()
    if not current_lt in favorite_list.long_term_objects.all():
        Favorite.objects.get(user=request.user.id).long_term_objects.add(Flat.objects.get(id=realty_id))
        return HttpResponse('to', content_type='text/html')
    else:
        Favorite.objects.get(user=request.user.id).long_term_objects.remove(
            Flat.objects.get(id=realty_id))
        return HttpResponse('from', content_type='text/html')


class RegisterObject(View):
    def get(self, request):
        return render(request, 'app_premises/register_object.html')

    def post(self, request):
        return render(request, 'app_premises/register_object.html')
