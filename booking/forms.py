import re
from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Application, Review

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        min_length=6,
        max_length=30,
        help_text='Латинские буквы и цифры, минимум 6 символов.',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Ivan123',
            'autocomplete': 'username',
            'data-rule': 'username',
        })
    )
    password = forms.CharField(
        label='Пароль',
        min_length=8,
        help_text='Минимум 8 символов.',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Не менее 8 символов',
            'autocomplete': 'new-password',
            'data-rule': 'password',
        })
    )
    full_name = forms.CharField(
        label='ФИО',
        max_length=180,
        widget=forms.TextInput(attrs={
            'placeholder': 'Иванов Иван Иванович',
            'autocomplete': 'name',
            'data-rule': 'full_name',
        })
    )
    phone = forms.CharField(
        label='Контактный телефон',
        max_length=30,
        help_text='Формат: +7 (999) 123-45-67.',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (___) ___-__-__',
            'autocomplete': 'tel',
            'inputmode': 'tel',
            'data-phone-mask': 'true',
            'data-rule': 'phone',
        })
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'mail@example.ru',
            'autocomplete': 'email',
            'data-rule': 'email',
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.fullmatch(r'[A-Za-z0-9]{6,}', username) or not re.search(r'[A-Za-z]', username) or not re.search(r'\d', username):
            raise ValidationError('Логин должен содержать латинские буквы и цифры, минимум 6 символов.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой логин уже занят.')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать 8 символов и более.')
        return password

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        normalized = re.sub(r'[\s()\-]', '', phone)
        if not re.fullmatch(r'\+7\d{10}', normalized):
            raise ValidationError('Телефон укажите в формате +7XXXXXXXXXX.')
        return normalized

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким e-mail уже зарегистрирован.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class ApplicationForm(forms.ModelForm):
    conference_date = forms.DateField(
        label='Дата начала конференции',
        input_formats=['%Y-%m-%d', '%d.%m.%Y'],
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Application
        fields = ['room', 'conference_date', 'payment_method']
        labels = {'room': 'Помещение', 'payment_method': 'Способ оплаты'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['conference_date'].widget.attrs['min'] = date.today().isoformat()

    def clean_conference_date(self):
        conference_date = self.cleaned_data['conference_date']
        if conference_date < date.today():
            raise ValidationError('Дата конференции не может быть в прошлом.')
        return conference_date

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        labels = {'rating': 'Оценка', 'text': 'Отзыв'}
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишите качество полученной услуги'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Оценка должна быть от 1 до 5.')
        return rating
