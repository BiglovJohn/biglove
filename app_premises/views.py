import datetime

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from .models import RealtyObject, Reservation, Photos, RealtyOptions
from .forms import ReservationForm, PriseFilterForm, DropdownFilterForm, RealtyTypeCheckBoxForm, \
    OptionFilterForm, InRoomOptionFilterForm, FoodOptionFilterForm, RealtyObjectForm, PhotosForm, BookCancelForm, \
    PayTypeForm

from app_profiler.models import CustomUser
from app_profiler.forms import RegisterForm, AuthForm
from app_comments.forms import CommentsForm
from app_comments.models import Comments
from app_companies.models import CompanyProfile


def main_realty_list(request):
    """
        Получаем параметры с index.html форм и по ним фильтруем поисковую выдачу:
        - Страна
        - Город
    """
    if 'search' in request.GET or 'realty_list__search' in request.POST or request.method == 'GET':
        if request.GET.get('q') is None:
            query = request.POST.get('q')
        else:
            query = request.GET.get('q')

        realty_list = RealtyObject.objects.filter(
            Q(realty_country__iregex=query) | Q(realty_city__iregex=query))

        """Фильтрация 'Сначала дорогое', ..."""
        main_filter = DropdownFilterForm(request.POST)
        if main_filter.is_valid():
            if main_filter.cleaned_data['popular_first'] == 'i':
                realty_list = realty_list.order_by('realty_price')

            if main_filter.cleaned_data['popular_first'] == 'x':
                realty_list = realty_list.order_by('-realty_price')

            if main_filter.cleaned_data['popular_first'] == 'p':
                realty_list = realty_list.order_by('-realty_book_count')

        """Фильтрация по диапазону цен"""
        price_filter = PriseFilterForm(request.POST)
        if price_filter.is_valid():
            if price_filter.cleaned_data['min_price']:
                realty_list = realty_list.filter(realty_price__gte=price_filter.cleaned_data['min_price'])

            if price_filter.cleaned_data['max_price']:
                realty_list = realty_list.filter(realty_price__lte=price_filter.cleaned_data['max_price'])

        """Фильтрация по типам помещений"""
        realty_type_checkbox = RealtyTypeCheckBoxForm(request.POST)

        realty_type_index = ['h', 'c', 'a', 'ah', 'gh', 'k', 'v', 'kp', 'gp']
        type_result_list = []

        if realty_type_checkbox.is_valid():
            for _type in realty_type_index:
                if _type in realty_type_checkbox.cleaned_data['realty_type']:
                    type_result_list.append(_type)

            if len(type_result_list) == 0:
                pass
            else:
                realty_list = realty_list.filter(realty_type__in=type_result_list)

        all_realty = RealtyObject.objects.all()  # Список всех объектов недвижимости для работы с фильтрами

        """Фильтрация по опциям питания"""
        food_options_checkbox = FoodOptionFilterForm(request.POST)
        food_type_list = []

        if food_options_checkbox.is_valid():
            for realty in all_realty:
                if realty.food_options in food_options_checkbox.cleaned_data['option']:
                    food_type_list.append(realty.id)
            if len(food_type_list) == 0:
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
            if len(book_type_list) == 0:
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

        """Помечаем забронированные объекты в искомые даты"""
        if request.method == 'GET':
            searched_check_in = datetime.datetime.strptime(request.GET.get('check_in'), "%d.%m.%Y").date()
            searched_check_out = datetime.datetime.strptime(request.GET.get('check_out'), "%d.%m.%Y").date()
        else:
            searched_check_in = datetime.datetime.strptime(request.POST.get('check_in'), "%d.%m.%Y").date()
            searched_check_out = datetime.datetime.strptime(request.POST.get('check_out'), "%d.%m.%Y").date()

        reservations_list = Reservation.objects.select_related('realty')

        reservation_set = []
        for reservation in reservations_list:
            if searched_check_out > reservation.check_in and searched_check_in < reservation.check_out \
                    or reservation.check_in < searched_check_out < reservation.check_out \
                    or reservation.check_in <= searched_check_in < reservation.check_out \
                    or searched_check_in == reservation.check_in and searched_check_out == reservation.check_out \
                    or searched_check_in <= reservation.check_in and searched_check_out >= reservation.check_out \
                    or searched_check_in < reservation.check_out < searched_check_out:
                reservation_set.append({'obj_id': reservation.realty.id, 'obj_check_in': str(reservation.check_in),
                                        'obj_check_out': str(reservation.check_out)})

        list_reserve_form = ReservationForm(initial={
            'check_in': searched_check_in,
            'check_out': searched_check_out
        }
        )

        return render(request, 'app_premises/realty_list.html',
                      {'realty_list': realty_list, 'price_filter': price_filter, 'main_filter': main_filter,
                       'realty_type_checkbox': realty_type_checkbox, 'hotel_filter_checkbox': hotel_filter_checkbox,
                       'reservation_set': reservation_set, 'list_reserve_form': list_reserve_form,
                       'room_filter_checkbox': room_filter_checkbox, 'food_options_checkbox': food_options_checkbox,
                       'book_filter': book_filter, 'pay_filter': pay_filter,
                       }
                      )


"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""


class RealtyDetailView(generic.DetailView):
    """Детальная информация по каждому объекту"""
    model = RealtyObject
    template_name = 'realty_detail.html'
    context_object_name = 'realty'
    queryset = RealtyObject.objects.prefetch_related('options')

    def get_success_url(self):
        return reverse('detail_view', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RealtyDetailView, self).get_form_kwargs(
            *args, **kwargs
        )
        return kwargs

    def get_context_data(self, *args, **kwargs):
        """Передача дополнительных моделей в шаблон через контекст"""
        context = super(RealtyDetailView, self).get_context_data(**kwargs)
        pk = kwargs['object'].id
        current_user = self.request.user.id
        current_realty = RealtyObject.objects.get(id=pk)

        # Получаем список опций конкретного отеля с категорией "В отеле"
        realty_in_hotel_options_name = [option.option_name for option in
                                        current_realty.options.filter(category='В отеле')]
        realty_in_hotel_options_category = [option.category for option in
                                            current_realty.options.filter(category='В отеле')]
        realty_options_list_in_hotel = list(zip(realty_in_hotel_options_category, realty_in_hotel_options_name))
        context['hotel_options'] = realty_options_list_in_hotel

        # Получаем список опций конкретного отеля с категорией "В номере"
        realty_in_room_options_name = [option.option_name for option in
                                       current_realty.options.filter(category='В номере')]
        realty_in_room_options_category = [option.category for option in
                                           current_realty.options.filter(category='В номере')]
        realty_options_list_in_room = list(zip(realty_in_room_options_category, realty_in_room_options_name))
        context['room_options'] = realty_options_list_in_room

        context['detail_photos'] = Photos.objects.filter(realty_obj=pk)
        context['detail_reserve_form'] = ReservationForm(
            initial={
                'realty': pk,
                'guest': current_user,
            }
        )
        context['comment_form'] = CommentsForm(
            initial={
                'user': current_user,
                'realty': pk,
            }
        )
        context['comments'] = Comments.objects.filter(realty=pk).order_by('-publish_at')
        return context

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and 'detail__send_feedback' in request.POST:
            slug = self.kwargs.get('slug')
            realty_id = RealtyObject.objects.get(slug=slug)
            comments_form = CommentsForm(request.POST)
            if comments_form.is_valid():
                comments_form.user_id = CustomUser.objects.get(id=request.user.id)
                comments_form.realty_id = realty_id.id
                comments_form.save()
        return redirect('app_premises:realty_detail', slug=self.kwargs.get('slug'))


class RealtyEditFromView(View):
    def get(self, request, slug):
        if 'delete_photo_button' in request.GET:
            pk = request.GET.get('delete_photo_button').split(', ')[1]
            Photos.objects.get(id=pk).delete()
            return redirect('app_premises:realty_edit', slug=self.kwargs.get('slug'))
        if request.user.is_authenticated and request.user.is_company:
            current_manager = CompanyProfile.objects.get(user=request.user.id)
            realty_edit = RealtyObject.objects.get(slug=slug)

            if realty_edit.company == current_manager:
                realty_edit_form = RealtyObjectForm(instance=realty_edit)
                upload_photos_form = PhotosForm(request.FILES, initial={'realty_obj': realty_edit.id})
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
            realty_edit = RealtyObject.objects.get(slug=slug)
            realty_edit_form = RealtyObjectForm(request.POST, instance=realty_edit)
            upload_photos_form = PhotosForm(request.POST, request.FILES, initial={'realty_obj': realty_edit.id})
            if realty_edit_form.is_valid():
                files = request.FILES.getlist('photo')
                realty_edit.save()
                for photo in files:
                    Photos.objects.create(realty_obj=realty_edit, photo=photo)

            elif 'realty_edit_submitting_photo' in request.POST:
                if upload_photos_form.is_valid():
                    files = request.FILES.getlist('photo')
                    for photo in files:
                        Photos.objects.create(realty_obj=realty_edit, photo=photo)
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


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""


class ReservationFormView(View):

    def get(self, request, *args, **kwargs):
        if 'to-reserve-page' in request.GET:
            if request.user.is_authenticated:
                realty = request.GET.get('to-reserve-page').split(', ')[0]
                current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
                current_user = CustomUser.objects.get(id=request.user.id)
                check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2],
                                                      "%Y-%m-%d").date()
                check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3],
                                                       "%Y-%m-%d").date()
                total_sum = (check_out - check_in).days * int(current_realty_price)
                reservation_form = ReservationForm(
                    initial={'realty': realty, 'guest': current_user, 'check_in': check_in, 'check_out': check_out,
                             'total_sum': total_sum, 'is_booked': False})
                realty_object_to_reserve_page = RealtyObject.objects.get(id=realty)
                photos = Photos.objects.filter(realty_obj=realty).first()

                return render(request, 'app_premises/reservation.html',
                              context={'reservation_form': reservation_form,
                                       'realty_object_to_reserve_page': realty_object_to_reserve_page,
                                       'current_user': current_user,
                                       'check_in': check_in,
                                       'check_out': check_out,
                                       'total_sum': total_sum,
                                       'photos': photos,
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
                realty_object_to_reserve_page = RealtyObject.objects.get(id=realty)
                photos = Photos.objects.filter(realty_obj=realty).first()
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
                reservation.guest = current_user
                reservation.realty = RealtyObject.objects.get(id=realty)
                reservation.is_booked = True
                reservation.save()
            else:
                pass

            return HttpResponseRedirect('/')

        if 'reserve__submit_login_form' in request.POST:
            realty = request.GET.get('to-reserve-page').split(', ')[0]
            current_realty_price = request.GET.get('to-reserve-page').split(', ')[1]
            check_in = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[2], "%Y-%m-%d").date()
            check_out = datetime.datetime.strptime(request.GET.get('to-reserve-page').split(', ')[3], "%Y-%m-%d").date()
            total_sum = (check_out - check_in).days * int(current_realty_price)
            realty_object_to_reserve_page = RealtyObject.objects.get(id=realty)
            photos = Photos.objects.filter(realty_obj=realty).first()
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

            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


def permission_denied(request):
    return render(request, '403.html')
