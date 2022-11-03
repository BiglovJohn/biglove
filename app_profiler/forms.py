import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser

User = get_user_model()

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)


class DatePickerForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'placeholder': f'{today.strftime("%d.%m.%Y")}'}),
                               input_formats=['%d.%m.%Y'], required=False)
    check_out = forms.DateField(widget=forms.DateInput(attrs={'placeholder': f'{tomorrow.strftime("%d.%m.%Y")}'}),
                                input_formats=['%d.%m.%Y'], required=False)


class AuthForm(forms.Form):
    email = forms.EmailField(required=True, help_text='Введите логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Введите логин'


class RegisterForm(UserCreationForm):
    """Переопределение формы регистрации главного родителя"""
    last_name = forms.CharField(max_length=25, required=False, label='Фамилия')
    first_name = forms.CharField(max_length=25, required=False, label='Имя')
    phone = forms.CharField(max_length=11, required=True, label='Номер телефона')
    email = forms.EmailField(label='Электронная почта', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)
    is_active = forms.BooleanField(required=True)
    is_company = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        """Задаём css class и help_text"""
        self.fields['password1'].widget.attrs['help_text'] = ''
        self.fields['password1'].widget.attrs['class'] = 'register-input'
        self.fields['password2'].widget.attrs['help_text'] = ''
        self.fields['password2'].widget.attrs['class'] = 'register-input'
        self.fields['first_name'].widget.attrs['class'] = 'register-input'
        self.fields['last_name'].widget.attrs['class'] = 'register-input'
        self.fields['phone'].widget.attrs['class'] = 'register-input'
        self.fields['email'].widget.attrs['class'] = 'register-input'
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_active'].widget.attrs['id'] = 'flexSwitchCheckDefault'
        self.fields['is_company'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_company'].widget.attrs['id'] = 'flexSwitchCheckDefault'

        """Задаём placeholder для полей регистрации"""
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['phone'].widget.attrs['placeholder'] = '+7(ХХХ)ХХХ-ХХ-ХХ'
        self.fields['email'].widget.attrs['placeholder'] = 'example@example.ru'

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'is_active', 'is_company']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class GuestForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['guest_book_count', 'guest_status']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        """Задаём css class"""
        self.fields['first_name'].widget.attrs['class'] = 'edit-account-input'
        self.fields['last_name'].widget.attrs['class'] = 'edit-account-input'
        self.fields['gender'].widget.attrs['class'] = 'edit-account-input'
        self.fields['phone'].widget.attrs['class'] = 'edit-account-input'
        self.fields['email'].widget.attrs['class'] = 'edit-account-input'
        # self.fields['email'].widget.attrs['disabled'] = True
        self.fields['birthday'].widget.attrs['class'] = 'edit-account-input'


class PasswordChangeCustomForm(PasswordChangeForm):
    pass
