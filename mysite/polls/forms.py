from django import forms
from django.core.exceptions import ValidationError

from .models import User

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='Email', max_length=254)
    first_name = forms.CharField(label="Имя", max_length=150)
    last_name = forms.CharField(label="Фамилия", max_length=150)
    avatar = forms.FileField(label='Загрузите свой аватар', widget=forms.FileInput, required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердить пароль", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой username уже занят')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Такой email уже занят')
        return email

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают')

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if self.cleaned_data.get("image"):
            user.avatar = self.cleaned_data.get("image")
        if commit:
            user.save()
            return user

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')

