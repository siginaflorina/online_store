from django import forms
from django.core.exceptions import ValidationError


# Create your forms here.
class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email: ", required=True, min_length=6, max_length=50)
    password = forms.CharField(label="Parola: ", widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(label="Confirmare parola: ", widget=forms.PasswordInput(), required=True)

    def check_passwords(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Parolele nu coincid')


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email: ", required=True, max_length=50)
    password = forms.CharField(label="Parola: ", widget=forms.PasswordInput())
