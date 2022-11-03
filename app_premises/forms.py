import datetime
from django import forms
from django.core.exceptions import ValidationError

from .models import RealtyObject, Reservation, RealtyOptions, Photos


list_of_id_in_hotel = [option.id for option in RealtyOptions.objects.filter(category='В отеле')]
list_of_names_in_hotel = [option.option_name for option in RealtyOptions.objects.filter(category='В отеле')]
_IN_HOTEL_OPTIONS = list(zip(list_of_id_in_hotel, list_of_names_in_hotel))


_FILTER_TYPE = [
    ('p', 'По популярности'),
    ('i', 'Сначала дешевле'),
    ('x', 'Сначала дороже'),
]

_REALTY_TYPE = [
    ('h', 'Отель'),
    ('c', 'Хостел'),
    ('a', 'Апартаменты'),
    ('ah', 'Апарт-отель'),
    ('gh', 'Гостевой дом'),
    ('k', 'Коттедж'),
    ('v', 'Вилла'),
    ('kp', 'Кемпинг'),
    ('gp', 'Глэмпинг'),
]

list_of_id_in_room = [option.id for option in RealtyOptions.objects.filter(category='В номере')]
list_of_names_in_room = [option.option_name for option in RealtyOptions.objects.filter(category='В номере')]

_IN_ROOM_OPTIONS = list(zip(list_of_id_in_room, list_of_names_in_room))

_FOOD_OPTIONS = [
    ('a', 'Завтрак включён'),
    ('b', 'Завтрак + обед или ужин включены'),
    ('c', 'Завтрак, обед и ужин включены'),
    ('d', 'Всё включено'),
    ('e', 'Питание не включено'),
]

# """Формируем список кортежей для поля CHICES"""
#
# list_of_latters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
#                    '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
#
# option_name_list = []
# option_name = RealtyOptions.objects.all()
# for option in option_name:
#     option_name_list.append(option.option_name)
#
# list_of_tuple_options_name = list(zip(list_of_latters, option_name_list))
# print(list_of_tuple_options_name)

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

"""Форма для создания объекта недвижимости"""


class RealtyObjectForm(forms.ModelForm):
    class Meta:
        model = RealtyObject
        fields = '__all__'
        exclude = ['created_at', 'realty_book_count', 'slug']

    def __init__(self, *args, **kwargs):
        super(RealtyObjectForm, self).__init__(*args, **kwargs)
        """Работа с классами формы"""
        self.fields['realty_name'].widget.attrs['class'] = 'create-realty-input'
        self.fields['realty_country'].widget.attrs['class'] = 'create-realty-input'
        self.fields['realty_region'].widget.attrs['class'] = 'create-realty-input'
        self.fields['realty_city'].widget.attrs['class'] = 'create-realty-input'
        self.fields['realty_address'].widget.attrs['class'] = 'create-realty-input'
        self.fields['realty_to_city'].widget.attrs['class'] = 'create-realty-input'
        self.fields['count_of_persons'].widget.attrs['class'] = 'create-realty-input-short'
        self.fields['realty_price'].widget.attrs['class'] = 'create-realty-input-short'
        self.fields['realty_area'].widget.attrs['class'] = 'create-realty-input-short'
        # self.fields['manager'] = forms.ModelChoiceField(
        #     required=True,
        #     queryset=ManagerProfile.objects.filter(referring_user=1))


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('check_in', 'check_out', 'total_sum')
        exclude = ['realty', 'guest', 'is_booked']

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['total_sum'].widget.attrs['readonly'] = True
        self.fields['check_in'].widget.attrs['placeholder'] = today.strftime("%d.%m.%Y")
        self.fields['check_out'].widget.attrs['placeholder'] = tomorrow.strftime("%d.%m.%Y")
        self.fields['check_in'].widget.attrs['autocomplete'] = 'Off'
        self.fields['check_out'].widget.attrs['autocomplete'] = 'Off'

    # def clean_check_in(self):
    #     check_in = self.cleaned_data['check_in']
    #     check_out = self.cleaned_data['check_out']
    #     print(check_out)
    #
    #     if check_in >= check_out:
    #         raise ValidationError('Ошибка в датах')


class PhotosForm(forms.ModelForm):

    class Meta:
        model = Photos
        fields = ('photo', )
        exclude = ['realty_obj', 'created_at']

    def __init__(self, *args, **kwargs):
        super(PhotosForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['multiple'] = True


class PriseFilterForm(forms.Form):
    min_price = forms.IntegerField(label='', required=False)
    max_price = forms.IntegerField(label='', required=False)


class DropdownFilterForm(forms.Form):
    popular_first = forms.ChoiceField(label='', choices=_FILTER_TYPE, required=False)


class RealtyTypeCheckBoxForm(forms.Form):
    realty_type = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_REALTY_TYPE,
    )

    def __init__(self, *args, **kwargs):
        super(RealtyTypeCheckBoxForm, self).__init__(*args, **kwargs)
        self.fields['realty_type'].widget.attrs['class'] = 'form-check-input'
        self.fields['realty_type'].widget.attrs['id'] = 'flexSwitchCheckDefault'


class OptionFilterForm(forms.Form):
    hotel_option = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_IN_HOTEL_OPTIONS,
    )

    def __init__(self, *args, **kwargs):
        super(OptionFilterForm, self).__init__(*args, **kwargs)
        self.fields['hotel_option'].widget.attrs['class'] = 'form-check-input'
        self.fields['hotel_option'].widget.attrs['id'] = 'flexCheckDefault'


class InRoomOptionFilterForm(forms.Form):
    room_option = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_IN_ROOM_OPTIONS,
    )

    def __init__(self, *args, **kwargs):
        super(InRoomOptionFilterForm, self).__init__(*args, **kwargs)
        self.fields['room_option'].widget.attrs['class'] = 'form-check-input'
        self.fields['room_option'].widget.attrs['id'] = 'in-room-options'


class FoodOptionFilterForm(forms.Form):
    option = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_FOOD_OPTIONS,
    )

    def __init__(self, *args, **kwargs):
        super(FoodOptionFilterForm, self).__init__(*args, **kwargs)
        self.fields['option'].widget.attrs['class'] = 'form-check-input'
        self.fields['option'].widget.attrs['id'] = 'food-options'


class BookCancelForm(forms.Form):
    _BOOK_CANCEL = [
        ('y', 'Беспл. отмена брони'),
        ('n', 'Нет беспл. отмены брони'),
    ]

    cancel_type = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_BOOK_CANCEL,
    )

    def __init__(self, *args, **kwargs):
        super(BookCancelForm, self).__init__(*args, **kwargs)
        self.fields['cancel_type'].widget.attrs['class'] = 'form-check-input'
        self.fields['cancel_type'].widget.attrs['id'] = 'cancel_type_options'


class PayTypeForm(forms.Form):
    _PAY_TYPE = [
        ('o', 'Оплата онлайн'),
        ('c', 'Оплата на месте')
    ]

    pay_type = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_PAY_TYPE,
    )

    def __init__(self, *args, **kwargs):
        super(PayTypeForm, self).__init__(*args, **kwargs)
        self.fields['pay_type'].widget.attrs['class'] = 'form-check-input'
        self.fields['pay_type'].widget.attrs['id'] = 'pay_type_options'
