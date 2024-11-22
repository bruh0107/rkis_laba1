from django import forms

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='Email', max_length=254)
    first_name = forms.CharField(label="Имя", max_length=150)