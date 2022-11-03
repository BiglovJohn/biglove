from django import forms
from .models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ['created_at', 'referring_user']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyProfileForm, self).__init__(*args, **kwargs)
        """Задаём css class"""
        self.fields['type'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['full_company_name'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['short_company_name'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['legal_address'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['actual_address'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['inn'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['kpp'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['ogrn'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['bank_account'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['bank_name'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['kor_account'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['bic'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['director'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['company_phone'].widget.attrs['class'] = 'edit-manager-input'
        self.fields['company_email'].widget.attrs['class'] = 'edit-manager-input'
