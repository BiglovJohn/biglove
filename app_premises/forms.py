import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import FurnitureModel, TechniqueModel, Flat
from .models import Camp, Reservation, RealtyOptions, Photos


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

# """Формируем список кортежей для поля CHOICES"""
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

""" Форма для создания объекта недвижимости типа 'Кемпинг' """


class HolidayHouseForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = '__all__'
        exclude = ['created_at', 'realty_book_count', 'is_favorites', 'views_count']

    def __init__(self, *args, **kwargs):
        super(HolidayHouseForm, self).__init__(*args, **kwargs)
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
        self.fields['region_center'].widget.attrs['class'] = 'create-realty-input-short'
        self.fields['arriving_time'].widget.attrs['class'] = 'create-realty-input'
        self.fields['departure_time'].widget.attrs['class'] = 'create-realty-input'
        # self.fields['company'] = forms.ModelChoiceField(
        #     required=True,
        #     queryset=ManagerProfile.objects.filter(referring_user=1))


class CreateHolidayHouseForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = '__all__'
        exclude = ['created_at', 'realty_book_count', 'is_favorites', 'views_count', 'slug']

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm, self).__init__(*args, **kwargs)
        """Работа с классами формы"""

        self.fields['realty_country'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['realty_region'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['realty_city'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['realty_address'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['realty_to_city'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['count_of_persons'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['realty_price'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['realty_area'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['region_center'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['arriving_time'].widget.attrs['class'] = 'hh_realty_create__input'
        self.fields['departure_time'].widget.attrs['class'] = 'hh_realty_create__input'

        self.fields['realty_name'].widget.attrs['class'] = 'form-control'
        self.fields['realty_name'].widget.attrs['required'] = True
        self.fields['realty_name'].widget.attrs['placeholder'] = 'Мезмайская пустошь'


class CreateHolidayHouseForm1(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ('realty_name', 'company')

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm1, self).__init__(*args, **kwargs)
        """Работа с классами формы"""

        self.fields['realty_name'].widget.attrs['class'] = 'form-control'
        self.fields['realty_name'].widget.attrs['required'] = True
        self.fields['realty_name'].widget.attrs['placeholder'] = 'Мезмайская пустошь'


class CreateHolidayHouseForm2(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ('realty_country', 'realty_city', 'realty_address', 'ind')

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm2, self).__init__(*args, **kwargs)
        """Работа с классами формы"""

        self.fields['ind'].widget.attrs['class'] = 'form-control'
        self.fields['ind'].widget.attrs['required'] = True
        self.fields['ind'].widget.attrs['placeholder'] = '350000'

        self.fields['realty_country'].widget.attrs['class'] = 'form-control'
        self.fields['realty_country'].widget.attrs['required'] = True
        self.fields['realty_country'].widget.attrs['placeholder'] = 'Россия'

        self.fields['realty_city'].widget.attrs['class'] = 'form-control'
        self.fields['realty_city'].widget.attrs['required'] = True
        self.fields['realty_city'].widget.attrs['placeholder'] = 'Москва'

        self.fields['realty_address'].widget.attrs['class'] = 'form-control'
        self.fields['realty_address'].widget.attrs['required'] = True
        self.fields['realty_address'].widget.attrs['placeholder'] = 'пр. Писателя Знаменского, 6'


class CreateHolidayHouseForm3(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ('count_of_persons', 'realty_area', 'realty_type', 'book_cancel', 'pay_type', 'food_options', 'stars')

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm3, self).__init__(*args, **kwargs)
        """Работа с классами формы"""

        self.fields['count_of_persons'].widget.attrs['class'] = 'form-control'
        self.fields['count_of_persons'].widget.attrs['required'] = True

        self.fields['realty_type'].widget.attrs['class'] = 'form-control'
        self.fields['realty_type'].widget.attrs['required'] = True

        self.fields['realty_area'].widget.attrs['class'] = 'form-control'
        self.fields['realty_area'].widget.attrs['required'] = True

        self.fields['stars'].widget.attrs['class'] = 'form-control'
        self.fields['stars'].widget.attrs['required'] = True

        self.fields['book_cancel'].widget.attrs['required'] = True
        self.fields['book_cancel'].widget.attrs['id'] = 'book_cancel_create_camp'
        self.fields['book_cancel'].widget.attrs['class'] = 'form-select'
        self.fields['pay_type'].widget.attrs['required'] = True
        self.fields['pay_type'].widget.attrs['id'] = 'pay_type_create_camp'
        self.fields['pay_type'].widget.attrs['class'] = 'form-select'
        self.fields['food_options'].widget.attrs['required'] = True
        self.fields['food_options'].widget.attrs['id'] = 'food_options_create_camp'
        self.fields['food_options'].widget.attrs['class'] = 'form-select'


class CreateHolidayHouseForm4(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ('options',)

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm4, self).__init__(*args, **kwargs)
        """Работа с классами формы"""

        self.fields['options'].widget.attrs['required'] = True


class CreateHolidayHouseForm5(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ('arriving_time', 'departure_time')

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm5, self).__init__(*args, **kwargs)
        """Работа с классами формы"""

        self.fields['arriving_time'].widget.attrs['class'] = 'form-control'
        self.fields['departure_time'].widget.attrs['class'] = 'form-control'


class CreateHolidayHouseForm6(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ('full_description',)

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm6, self).__init__(*args, **kwargs)
        """ Работа с классами формы """


class CreateHolidayHouseForm7(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ('realty_price',)

    def __init__(self, *args, **kwargs):
        super(CreateHolidayHouseForm7, self).__init__(*args, **kwargs)
        """ Работа с классами формы """
        self.fields['realty_price'].widget.attrs['class'] = 'form-control'


""" Формы связанные с резервированием """


class ReservationForm(forms.ModelForm):
    """ Форма резервирования объекта """

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


class ReservationListSearchForm(forms.Form):
    """ Форма резервирования для вывода date picker на главную страницу """

    check_in = forms.DateField(required=False)
    check_out = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(ReservationListSearchForm, self).__init__(*args, **kwargs)
        self.fields['check_in'].widget.attrs['placeholder'] = today.strftime("%d.%m.%Y")
        self.fields['check_out'].widget.attrs['placeholder'] = tomorrow.strftime("%d.%m.%Y")
        self.fields['check_in'].widget.attrs['autocomplete'] = 'Off'
        self.fields['check_out'].widget.attrs['autocomplete'] = 'Off'
        self.fields['check_in'].widget.attrs['required'] = False
        self.fields['check_out'].widget.attrs['required'] = False


class ReservationIndexSearchForm(forms.Form):
    """ Форма резервирования для вывода date picker на главную страницу """

    check_in = forms.DateField(required=False)
    check_out = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(ReservationIndexSearchForm, self).__init__(*args, **kwargs)
        self.fields['check_in'].widget.attrs['placeholder'] = today.strftime("%d.%m.%Y")
        self.fields['check_out'].widget.attrs['placeholder'] = tomorrow.strftime("%d.%m.%Y")
        self.fields['check_in'].widget.attrs['autocomplete'] = 'Off'
        self.fields['check_out'].widget.attrs['autocomplete'] = 'Off'
        self.fields['check_in'].widget.attrs['id'] = 'main_search_in'
        self.fields['check_out'].widget.attrs['id'] = 'main_search_out'
        self.fields['check_in'].widget.attrs['required'] = False
        self.fields['check_out'].widget.attrs['required'] = False


""" Формы связанные с фотографиями """


class PhotosForm(forms.ModelForm):

    class Meta:
        model = Photos
        fields = ('photo', )
        exclude = ['realty_obj', 'created_at']

    def __init__(self, *args, **kwargs):
        super(PhotosForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['multiple'] = True


""" Формы связанные с фильтрами """


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


""" ОБЪЕКТЫ НА ДЛИТЕЛЬНЫЙ СРОК """


list_of_furniture_id = [furniture.id for furniture in FurnitureModel.objects.all()]
list_of_furniture_names = [furniture.name for furniture in FurnitureModel.objects.all()]
_FURNITURE = list(zip(list_of_furniture_id, list_of_furniture_names))

list_of_technique_id = [technique.id for technique in TechniqueModel.objects.all()]
list_of_technique_names = [technique.name for technique in TechniqueModel.objects.all()]
_TECHNIQUE = list(zip(list_of_technique_id, list_of_technique_names))


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = '__all__'
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super(FlatForm, self).__init__(*args, **kwargs)
        """Работа с классами формы"""
        self.fields['realty_country'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['realty_region'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['realty_city'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['realty_address'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['city_area'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['micro_city_area'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['house_number'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['house_korpus'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['house_korpus'].widget.attrs['placeholder'] = 'Лит. А | Корп. 1 | Блок Б'

        self.fields['rooms_count'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['floor'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['floor_count'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['deposit'].widget.attrs['class'] = 'lt_realty_create__input'

        self.fields['realty_price'].widget.attrs['class'] = 'lt_realty_create__input'
        self.fields['realty_area'].widget.attrs['class'] = 'lt_realty_create__input'
        # self.fields['company'] = forms.ModelChoiceField(
        #     required=True,
        #     queryset=ManagerProfile.objects.filter(referring_user=1))


class DropdownFilterLongTermForm(forms.Form):
    _FILTER_TYPE = [
        ('p', 'Сначала новые'),
        ('i', 'Сначала дешевле'),
        ('x', 'Сначала дороже'),
    ]

    filter_param = forms.ChoiceField(label='', choices=_FILTER_TYPE, required=False)


class AreaFilterForm(forms.Form):
    min_area = forms.IntegerField(label='', required=False)
    max_area = forms.IntegerField(label='', required=False)


class FloorFilterForm(forms.Form):
    min_floor = forms.IntegerField(label='', required=False)
    max_floor = forms.IntegerField(label='', required=False)


class RulesFilterForm(forms.Form):
    _RULES = [
        ('1', 'Можно с детьми'),
        ('2', 'Можно с животными'),
        ('3', 'Можно курить'),
    ]
    rule_option = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_RULES,
    )

    def __init__(self, *args, **kwargs):
        super(RulesFilterForm, self).__init__(*args, **kwargs)
        self.fields['rule_option'].widget.attrs['class'] = 'form-check-input'
        self.fields['rule_option'].widget.attrs['id'] = 'flexCheckDefault'


class BathroomFilterForm(forms.Form):
    _BATHROOM = [
        ('1', 'Раздельный'),
        ('2', 'Совмещенный'),
        ('3', 'Не важно')
    ]
    bathroom_option = forms.ChoiceField(
        choices=_BATHROOM,
        widget=forms.RadioSelect,
        label='',
        required=False,
    )


class FurnitureFilterForm(forms.Form):
    furniture_option = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_FURNITURE,
    )

    def __init__(self, *args, **kwargs):
        super(FurnitureFilterForm, self).__init__(*args, **kwargs)
        self.fields['furniture_option'].widget.attrs['class'] = 'form-check-input'
        self.fields['furniture_option'].widget.attrs['id'] = 'flexCheckDefault2'


class TechniqueFilterForm(forms.Form):
    technique_option = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=_TECHNIQUE,
    )

    def __init__(self, *args, **kwargs):
        super(TechniqueFilterForm, self).__init__(*args, **kwargs)
        self.fields['technique_option'].widget.attrs['class'] = 'form-check-input'
        self.fields['technique_option'].widget.attrs['id'] = 'flexCheckDefault3'
