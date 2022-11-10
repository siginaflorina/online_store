from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from .models import User
from .models import Role
from .forms import RegistrationForm
from .forms import LoginForm
from django.views.generic import TemplateView

# Create your views here.
from django.views.generic import TemplateView


class About_usTemplateView(TemplateView):
    template_name = "app.html"

class ContactTemplateView(TemplateView):
    template_name = "app.html"

def home(request):
    # legatura cu fisierul template index.html
    return render(request, '../templates/app.html')

class HomeTemplateView(TemplateView):
    template_name = "app.html"

def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # aici ne luam role-ul pentru un client
            client_role = Role.objects.filter(name="client").first()
            # crearea unui user, cu datele din form-ul de inregistrare
            user = User(email=form.cleaned_data['email'], role=client_role)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Contul s-a creat cu succes!")
            return redirect(login)
        else:
            print("NOT OK")
            print(form.errors.as_data())
            messages.error(request, "Erori")

    return render(request, '../templates/register.html', {'form': form})


def login(request):
    form = LoginForm()
    return render(request, '../templates/login.html', {'form': form})


def app(request):
    return render(request, '../templates/app.html')


def users(request):
    all_users = User.objects.all()
    return HttpResponse('<br/>'.join([str(user) for user in all_users]))


def roles(request):
    Role.objects.all().delete()
    role1 = Role(name="client")
    role2 = Role(name="admin")
    role1.save()
    role2.save()
    all_roles = Role.objects.all()

    return HttpResponse('<br/>'.join([str(role) for role in all_roles]))
