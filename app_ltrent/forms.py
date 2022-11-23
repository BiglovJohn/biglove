from django import forms
from .models import FurnitureModel, TechniqueModel, LongTermRentObject, LongTermPhotos

list_of_furniture_id = [furniture.id for furniture in FurnitureModel.objects.all()]
list_of_furniture_names = [furniture.name for furniture in FurnitureModel.objects.all()]
_FURNITURE = list(zip(list_of_furniture_id, list_of_furniture_names))

list_of_technique_id = [technique.id for technique in TechniqueModel.objects.all()]
list_of_technique_names = [technique.name for technique in TechniqueModel.objects.all()]
_TECHNIQUE = list(zip(list_of_technique_id, list_of_technique_names))


class LongTermRentObjectForm(forms.ModelForm):
    class Meta:
        model = LongTermRentObject
        fields = '__all__'
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super(LongTermRentObjectForm, self).__init__(*args, **kwargs)
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


class LongTermPhotosForm(forms.ModelForm):

    class Meta:
        model = LongTermPhotos
        fields = ('photo', )
        exclude = ['long_term_obj', 'created_at']

    def __init__(self, *args, **kwargs):
        super(LongTermPhotosForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['multiple'] = True


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
