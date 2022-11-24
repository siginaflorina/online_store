from django import forms
from django.core.exceptions import ValidationError


# Create your forms here.
class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email: ', required=True, min_length=6, max_length=50)
    password = forms.CharField(label='Parola: ', widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(label='Confirmare parola: ', widget=forms.PasswordInput(), required=True)

    def check_passwords(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Parolele nu coincid')


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email: ', required=True, max_length=50)
    password = forms.CharField(label='Parola: ', widget=forms.PasswordInput())


# class CheckoutForm(forms.Form):
#     use_user_address = forms.BooleanField(label='Foloseste adresa adaugata in detalii cont', required=False)
#     address = forms.CharField(
#         label='Adresa',
#         widget=forms.Textarea(
#             attrs={
#                 'rows': '4',
#                 'placeholder': 'Introdu adresa...'
#             }
#         ),
#         max_length=500,
#         required=False)
#     message = forms.CharField(
#         label='Mesaj (optional)',
#         widget=forms.Textarea(
#             attrs={
#                 'rows': '4',
#                 'placeholder': 'Introdu mesaj...'
#             }
#         ),
#         max_length=500,
#         required=False
#     )
#
#     address.widget.attrs.pop('cols')
#     message.widget.attrs.pop('cols')

class UserPasswordForm(forms.Form):
    old_password = forms.CharField(
        label='Parola actuala: ',
        widget=forms.PasswordInput(attrs={'placeholder': 'Introdu parola actuala...'}),
        required=True
    )
    new_password = forms.CharField(
        label='Parola noua: ',
        widget=forms.PasswordInput(attrs={'placeholder': 'Introdu parola noua...'}),
        required=True
    )
    confirm_password = forms.CharField(
        label='Confirmare parola noua: ',
        widget=forms.PasswordInput(attrs={'placeholder': 'Introdu confirmarea parolei...'}),
        required=True
    )


class UserDetailsForm(forms.Form):
    last_name = forms.CharField(
        label='Nume:',
        widget=forms.TextInput(attrs={'placeholder': 'Introdu nume...'}),
        max_length=50,
        required=False
    )
    first_name = forms.CharField(
        label='Prenume:',
        widget=forms.TextInput(attrs={'placeholder': 'Introdu prenume...'}),
        max_length=30,
        required=False
    )
    city = forms.CharField(
        label='Oras:',
        widget=forms.TextInput(attrs={'placeholder': 'Introdu oras...'}),
        max_length=100,
        required=False
    )
    address = forms.CharField(
        label='Adresa:',
        widget=forms.Textarea(attrs={'placeholder': 'Introdu adresa...'}),
        max_length=500,
        required=False
    )
    preferred_communication_channel = forms.ChoiceField(
        label='Canalul preferat de comunicare:',
        choices=[('mail', 'MAIL'), ('email', 'EMAIL')],
        required=False
    )
