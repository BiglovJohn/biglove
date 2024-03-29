import datetime

from django.db.models import Count, Sum
from .forms import ReservationIndexSearchForm
from .models import Camp, RealtyOptions, Reservation, Photos, Flat


def render_reservation_form(request):
    """Проверяем залогинен ли наш юзер"""
    if 'search' in request.GET:
        """
            Если он жмакнул кнопку с GET запросом по имени search со страницы index и юзер не компания, то получаем
             форму резервирования и список броней текущего пользователя.
        """
        reserve_form = ReservationIndexSearchForm()
        reservation_list = Reservation.objects.filter(guest=request.user.id)
        return {'reserve_form': reserve_form, 'reservation_list': reservation_list}
    elif 'check-is-reserve-available' in request.GET:
        """
            Ежели ткнули кнопку с указаным выше именем из шаблона detail-view то получаем заполненную форму фрони
            со всеми нужными параметрами которые мы берем из передаваемых в запросе значений:
            
                pk(int): это id объекта недвижимости
                reserve_sum(int): передаём параметр цены номера за сутки
                check_in(str): переводим строку с датой в объект даты для дальнейших манипуляций
                check_out(str): переводим строку с датой в объект даты для дальнейших манипуляций
                total_sum(int): Считаем сколько дней бронь, умножаем на цену
                current_user(int): id текущего пользователя
        """
        pk = request.GET.get('check-is-reserve-available').split(', ')[0]
        reserve_sum = request.GET.get('check-is-reserve-available').split(', ')[1]
        check_in = datetime.datetime.strptime(request.GET.get('check_in'), "%d.%m.%Y").date()
        check_out = datetime.datetime.strptime(request.GET.get('check_out'), "%d.%m.%Y").date()
        total_sum = (check_out - check_in).days * int(reserve_sum)
        current_user = request.user.id
        detail_reserve_form_filled = ReservationIndexSearchForm(
            initial={'realty': pk, 'guest': current_user, 'check_in': check_in, 'check_out': check_out,
                     'total_sum': total_sum})

        reservations_list = Reservation.objects.filter(realty=pk).select_related('realty')

        reservation_set_detail = []
        for reservation in reservations_list:
            if check_out > reservation.check_in and check_in < reservation.check_out \
                    or reservation.check_in < check_out < reservation.check_out \
                    or reservation.check_in <= check_in < reservation.check_out \
                    or check_in == reservation.check_in and check_out == reservation.check_out \
                    or check_in <= reservation.check_in and check_out >= reservation.check_out \
                    or check_in < reservation.check_out < check_out:
                reservation_set_detail.append(
                    {'obj_id': reservation.realty.id, 'obj_check_in': str(reservation.check_in),
                     'obj_check_out': str(reservation.check_out)})

        return {'detail_reserve_form_filled': detail_reserve_form_filled,
                'reservation_set_detail': reservation_set_detail,
                'pk': int(pk), 'check_in': str(check_in), 'check_out': str(check_out)}

    else:
        reserve_form = ReservationIndexSearchForm()
        return {'reserve_form': reserve_form}


def render_realty_object_to_profile(request):
    """Вывод объектов УК в профиль"""
    realty_objects_to_profile = Camp.objects.filter(company=request.user.id)
    lt_realty_objects_to_profile = Flat.objects.filter(company=request.user.id)
    reservations_list = Reservation.objects.filter(
        realty__in=realty_objects_to_profile).select_related('realty').select_related('guest')
    total_company_sum = Reservation.objects.filter(realty__in=realty_objects_to_profile).aggregate(Sum('total_sum'))[
        'total_sum__sum']

    return {'realty_objects_to_profile': realty_objects_to_profile,
            'lt_realty_objects_to_profile': lt_realty_objects_to_profile,
            'reservations_list': reservations_list,
            'total_company_sum': total_company_sum}


def render_today_and_tomorrow(request):
    check_in_to_detail = request.GET.get('check_in')
    check_out_to_detail = request.GET.get('check_out')
    return {'check_in_to_detail': check_in_to_detail, 'check_out_to_detail': check_out_to_detail}
