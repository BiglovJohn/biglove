import datetime
import re
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser


User = get_user_model()

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)


class AuthForm(forms.Form):
    """
        Форма авторизации и аутентификации

        Attributes:
            email: str
                Current user email
            password: str
                Current user password
    """
    email = forms.EmailField(required=True, help_text='Введите логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    # user = CustomUser.objects.last()
    user_id = 0

    """Переопределение формы регистрации главного родителя"""
    last_name = forms.CharField(max_length=25, required=False, label='Фамилия')
    first_name = forms.CharField(max_length=25, required=False, label='Имя')
    phone = forms.CharField(max_length=12, required=True, label='Номер телефона')
    email = forms.EmailField(label='Электронная почта', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)
    is_active = forms.BooleanField(required=True)
    is_company = forms.BooleanField(required=False)
    slug = forms.CharField(max_length=30, initial=f'user{user_id}', label='Ник', required=True)
    birthday = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        """Задаём css class и help_text"""
        self.fields['password1'].widget.attrs['help_text'] = ''
        self.fields['password1'].widget.attrs['class'] = 'register-input'
        self.fields['password2'].widget.attrs['help_text'] = ''
        self.fields['password2'].widget.attrs['class'] = 'register-input'
        self.fields['first_name'].widget.attrs['class'] = 'register-input'
        self.fields['last_name'].widget.attrs['class'] = 'register-input'
        self.fields['slug'].widget.attrs['class'] = 'register-input'
        self.fields['phone'].widget.attrs['class'] = 'register-input'
        self.fields['email'].widget.attrs['class'] = 'register-input'
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_active'].widget.attrs['id'] = 'flexSwitchCheckDefault'
        self.fields['is_company'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_company'].widget.attrs['id'] = 'flexSwitchCheckDefault'
        self.fields['birthday'].widget.attrs['class'] = 'register-input'

        self.fields['slug'].widget.attrs['autocomplete'] = 'Off'

        """Задаём placeholder для полей регистрации"""
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['slug'].widget.attrs['placeholder'] = 'Придумайте имя пользователя'
        self.fields['phone'].widget.attrs['placeholder'] = '+7(ХХХ)ХХХ-ХХ-ХХ'
        self.fields['email'].widget.attrs['placeholder'] = 'example@example.ru'

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'slug', 'birthday', 'last_name', 'phone',
                  'is_active', 'is_company']


class RegisterForm1(UserCreationForm):
    # user = CustomUser.objects.last()
    user_id = 0

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email):
            self.add_error('email', 'Пользователь с такой почтой уже существует!')
        return email

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            self.add_error('password2', 'Введённые пароли не совпадают!')
        return password1

    def __init__(self, *args, **kwargs):
        super(RegisterForm1, self).__init__(*args, **kwargs)
        """Задаём css class и help_text"""
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['required'] = True
        self.fields['password1'].widget.attrs['help_text'] = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['required'] = True
        self.fields['password2'].widget.attrs['help_text'] = ''

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['required'] = True

        """Задаём placeholder для полей регистрации"""
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        self.fields['email'].widget.attrs['placeholder'] = 'example@example.ru'


class RegisterForm2(forms.Form):
    last_name = forms.CharField(max_length=25, label='Фамилия')
    first_name = forms.CharField(max_length=25, label='Имя')
    phone = forms.CharField(max_length=12, required=True, label='Номер телефона')
    slug = forms.CharField(max_length=30, label='Ник', required=True)
    birthday = forms.DateField(required=False)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if re.findall("\d+", first_name) or re.findall("\d+", last_name):
            self.add_error('first_name', 'Имя не может содержать цифры')
            self.add_error('last_name', 'Фамилия не может содержать цифры')
        return first_name

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if CustomUser.objects.filter(slug=slug):
            self.add_error('slug', 'Имя пользователя занято, выберите другое!')
        return slug

    def __init__(self, *args, **kwargs):
        super(RegisterForm2, self).__init__(*args, **kwargs)
        """Задаём css class и help_text"""

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['required'] = True
        self.fields['birthday'].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['required'] = False
        self.fields['birthday'].widget.attrs['id'] = 'register_form_id'

        """Задаём placeholder для полей регистрации"""
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['slug'].widget.attrs['placeholder'] = 'biglove'
        self.fields['birthday'].widget.attrs['placeholder'] = '24.11.1990'
        self.fields['phone'].widget.attrs['placeholder'] = '+79999999999'


class RegisterForm3(forms.Form):
    is_active = forms.BooleanField(required=True)
    is_company = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm3, self).__init__(*args, **kwargs)
        """Задаём css class и help_text"""

        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_active'].widget.attrs['id'] = 'flexSwitchCheckDefault'
        self.fields['is_active'].widget.attrs['required'] = True
        self.fields['is_company'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_company'].widget.attrs['id'] = 'flexSwitchCheckDefault'
        self.fields['is_company'].widget.attrs['required'] = False


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
        self.fields['slug'].widget.attrs['placeholder'] = '/username'
        self.fields['slug'].widget.attrs['class'] = 'edit-account-input'
        self.fields['birthday'].widget.attrs['class'] = 'edit-account-input'
        self.fields['telegram'].widget.attrs['class'] = 'edit-account-input'


class PasswordChangeCustomForm(PasswordChangeForm):
    pass


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyProfileForm, self).__init__(*args, **kwargs)
        """Задаём css class"""
        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['full_company_name'].widget.attrs['class'] = 'form-control'
        self.fields['short_company_name'].widget.attrs['class'] = 'form-control'
        self.fields['legal_address'].widget.attrs['class'] = 'form-control'
        self.fields['actual_address'].widget.attrs['class'] = 'form-control'
        self.fields['inn'].widget.attrs['class'] = 'form-control'
        self.fields['kpp'].widget.attrs['class'] = 'form-control'
        self.fields['ogrn'].widget.attrs['class'] = 'form-control'
        self.fields['bank_account'].widget.attrs['class'] = 'form-control'
        self.fields['bank_name'].widget.attrs['class'] = 'form-control'
        self.fields['kor_account'].widget.attrs['class'] = 'form-control'
        self.fields['bic'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['middle_name'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['nds'].widget.attrs['class'] = 'form-control'
        self.fields['passport_series'].widget.attrs['class'] = 'form-control'
        self.fields['passport_number'].widget.attrs['class'] = 'form-control'
        self.fields['passport_who'].widget.attrs['class'] = 'form-control'
        self.fields['passport_code'].widget.attrs['class'] = 'form-control'
        self.fields['passport_date'].widget.attrs['class'] = 'form-control'
