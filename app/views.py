import json
import random
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user
from django.contrib import messages
from .models import User
from .models import Role
from .models import Category
from .models import Product
from .models import Order
from .models import OrderLine
from .models import Favorite
from .forms import RegisterForm
from .forms import LoginForm
from .forms import UserDetailsForm
from .forms import UserPasswordForm

# Create your views here.


def home(request):
    # legatura cu fisierul template index.html
    return render(request, '../templates/index.html')


def register(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # aici ne luam role-ul pentru un client
            client_role = Role.objects.filter(name="client").first()
            # crearea unui user, cu datele din form-ul de inregistrare
            user = User(
                username=register_form.cleaned_data['email'],
                email=register_form.cleaned_data['email'],
                role=client_role
            )
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            messages.success(request, "Contul s-a creat cu succes!")
            return redirect(login)
        else:
            print(register_form.errors)
            messages.error(request, register_form.errors)

    return render(request, '../templates/register.html', {'register_form': register_form})


def login(request):
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = User.objects.filter(email=login_form.cleaned_data['email']).first()

            if user.check_password(login_form.cleaned_data['password']):
                auth_login(request, user)
                messages.success(request, "Te-ai autentificat cu succes")
                return redirect(app)
            else:
                messages.error(request, "Parola este eronata, incearca din nou!")
        else:
            print("NOT OK")
            print(login_form.errors)
            messages.error(request, login_form.errors)

    return render(request, '../templates/login.html', {'login_form': login_form})


@login_required(login_url='/login')
def app(request):
    current_user = User.objects.filter(user_ptr_id=get_user(request).id).first()

    user_details_form = UserDetailsForm(
        initial={
            'last_name': current_user.last_name,
            'first_name': current_user.first_name,
            'city': current_user.city,
            'address': current_user.address,
            'preferred_communication_channel': current_user.preferred_communication_channel
        }
    )
    user_password_form = UserPasswordForm()

    context = {
        'user_details_form': user_details_form,
        'user_password_form': user_password_form
    }

    for p in Product.objects.all():
        category_name = f'products_category_{p.category.name}'
        if category_name in context:
            if len(context[category_name]) < 10:
                context[category_name].append(p.dict)
        else:
            context[category_name] = [p.dict]

    return render(request, '../templates/app.html', context)


@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    messages.success(request, 'Ai iesit din aplicatie cu succes!')
    return redirect(login)


@login_required(login_url='/login')
def category(request, name):
    category_obj = Category.objects.filter(name=name).first()
    context = {
        'category': name.capitalize()
    }
    for p in Product.objects.filter(category=category_obj).all():
        if 'products' in context:
            context['products'].append(p.dict)
        else:
            context['products'] = [p.dict]

    return render(request, '../templates/category.html', context)


@login_required(login_url='/login')
def favorites(request):
    favorite_objs = Favorite.objects.filter(client=get_user(request)).all()

    context = {}
    for favorite_obj in favorite_objs:
        if 'products' in context:
            context['products'].append(favorite_obj.product.dict)
        else:
            context['products'] = [favorite_obj.product.dict]

    return render(request, '../templates/favorites.html', context=context)


@login_required(login_url='/login')
def product(request, id_product):
    return render(request, '../templates/product.html')


@login_required(login_url='/login')
def api_product(request, id_product):
    product_obj = Product.objects.filter(id=id_product).first()
    return JsonResponse(product_obj.dict)


@login_required(login_url='/login')
def api_users(request):
    all_users = User.objects.all()
    return HttpResponse('<br/>'.join([str(user) for user in all_users]))


@login_required(login_url='/login')
def api_roles(request):
    Role.objects.all().delete()
    role1 = Role(name="client")
    role2 = Role(name="admin")
    role1.save()
    role2.save()
    all_roles = Role.objects.all()

    return HttpResponse('<br/>'.join([str(role) for role in all_roles]))


@login_required(login_url='/login')
def api_products(request):
    Category.objects.all().delete()
    Product.objects.all().delete()

    list_products_data = [
        {
            'title': 'Apa Borsec plata 2L',
            'image': 'apa-borsec-plata-2l.png',
            'price': 2.75,
            'category': 'apa'
        },
        {
            'title': 'Apa Borsec minerala 1.5L',
            'image': 'apa-borsec-minerala-15l.png',
            'price': 2.65,
            'category': 'apa'
        },
        {
            'title': 'Apa Aquatique plata 0.5L',
            'image': 'apa-aquatique-plata-05l.png',
            'price': 5.00,
            'category': 'apa'
        },
        {
            'title': 'Apa Aquatique plata 1L',
            'image': 'apa-aquatique-apa-plata-1l.png',
            'price': 3.00,
            'category': 'apa'
        },
        {
            'title': 'Apa Aquatique plata 2L',
            'image': 'apa-aquatique-apa-plata-2l.png',
            'price': 3.50,
            'category': 'apa'
        },
        {
            'title': 'Apa Aquatique plata 5L',
            'image': 'apa-aquatique-plata-5l.png',
            'price': 9.00,
            'category': 'apa'
        },
        {
            'title': 'Apa Bucovina plata 0.5L',
            'image': 'apa-bucovina-plata-05l.png',
            'price': 4.50,
            'category': 'apa'
        },
        {
            'title': 'Apa Bucovina plata 0.7L',
            'image': 'apa-bucovina-plata-07l.png',
            'price': 5.00,
            'category': 'apa'
        },
        {
            'title': 'Apa Bucovina plata 2L',
            'image': 'apa-bucovina-plata-2l.png',
            'price': 4.00,
            'category': 'apa'
        },
        {
            'title': 'Apa Bucovina plata 5L',
            'image': 'apa-bucovina-plata-5l.png',
            'price': 9.90,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Minerala 0.5L',
            'image': 'apa-carpatica-minerala-05l.png',
            'price': 4.30,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Minerala 0.7L',
            'image': 'apa-carpatica-minerala-07l.png',
            'price': 3.90,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Minerala 0.33L',
            'image': 'apa-carpatica-minerala-033l.png',
            'price': 4.20,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Minerala Forte 0.7L',
            'image': 'apa-carpatica-forte-minerala-07l.png',
            'price': 5.30,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Plata 0.5L',
            'image': 'apa-carpatica-plata-05l.png',
            'price': 4.90,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Plata 1L',
            'image': 'apa-carpatica-plata-1l.png',
            'price': 1.90,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Plata 2L',
            'image': 'apa-carpatica-plata-2l.png',
            'price': 2.90,
            'category': 'apa'
        },
        {
            'title': 'Apa Aqua Carpatica Plata 5L',
            'image': 'apa-carpatica-plata-5l.png',
            'price': 9.99,
            'category': 'apa'
        },
        {
            'title': 'Apa Acqua Panna Plata 1L',
            'image': 'apa-acqua-panna-plata-1l.png',
            'price': 7.00,
            'category': 'apa'
        },
        {
            'title': 'Rent equipment',
            'image': 'aparat.png',
            'price': 50.00,
            'category': 'servicii'
        },
        {
            'title': 'Buy equipment',
            'image': 'aparat.png',
            'price': 499.90,
            'category': 'servicii'
        },
        {
            'title': 'For your company',
            'image': 'business-logo.png',
            'price': 49.90,
            'category': 'servicii'
        },
        {
            'title': 'Maintenance',
            'image': 'maintance.png',
            'price': 75.00,
            'category': 'servicii'
        },
    ]

    list_new_products = []

    for product_data in list_products_data:
        product_category = Category.objects.filter(name=product_data['category']).first()
        if not product_category:
            product_category = Category(name=product_data['category'])
            product_category.save()
        new_product = Product(
            title=product_data['title'],
            image=product_data['image'],
            nr_stars=random.randint(0, 5),
            price=product_data['price'],
            category=product_category
        )
        new_product.save()
        list_new_products.append(new_product)

    return HttpResponse('<br/>'.join([str(new_product) for new_product in list_new_products]))


@login_required(login_url='/login')
def api_favorites(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = int(data['product_id'])
        product_obj = Product.objects.filter(id=product_id).first()
        favorite_obj = Favorite(product=product_obj, client=get_user(request))
        favorite_obj.save()
        return JsonResponse({'message': f'Produsul {product_obj.title} a fost adaugat la favorite!', 'messageType': 'success'})

    all_favorites = Favorite.objects.all()

    return HttpResponse('<br/>'.join([str(favorite) for favorite in all_favorites]))


@login_required(login_url='/login')
def api_orders(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_obj = Order(delivery_address=data['address'], message=data['message'], client=get_user(request))
        order_obj.save()

        total_cost = 0
        for product_data in data['products']:
            product_id = int(product_data['id'])
            nr_of_products = int(product_data['nr'])

            product_obj = Product.objects.filter(id=product_id).first()
            total_cost += product_obj.price * nr_of_products

            order_line = OrderLine(product=product_obj, number_of_products=nr_of_products, order=order_obj)
            order_line.save()

        order_obj.total_cost = total_cost
        order_obj.save()

        return JsonResponse({'message': 'Comanda a fost trimisa cu succes!', 'messageType': 'success'})

    all_orders = Order.objects.all()

    return HttpResponse('<br/>'.join([str(order) for order in all_orders]))


@login_required(login_url='/login')
def auth_change_user_details(request):
    if request.method == 'POST':
        current_user = User.objects.filter(user_ptr_id=get_user(request).id).first()

        user_details_form = UserDetailsForm(request.POST)

        if user_details_form.is_valid():
            current_user.last_name = user_details_form.cleaned_data['last_name']
            current_user.first_name = user_details_form.cleaned_data['first_name']
            current_user.city = user_details_form.cleaned_data['city']
            current_user.address = user_details_form.cleaned_data['address']
            current_user.preferred_communication_channel = user_details_form.cleaned_data['preferred_communication_channel']

            current_user.save()
            messages.success(request, 'Datele au fost schimbate cu succes!')
            return redirect(app)
        else:
            messages.error(request, user_details_form.errors)
            return redirect(app)


@login_required(login_url='/login')
def auth_change_user_password(request):
    if request.method == 'POST':
        current_user = User.objects.filter(user_ptr_id=get_user(request).id).first()

        user_password_form = UserPasswordForm(request.POST)

        if user_password_form.is_valid():
            if current_user.check_password(user_password_form.cleaned_data['old_password']):
                if user_password_form.cleaned_data['new_password'] == user_password_form.cleaned_data['confirm_password']:
                    current_user.set_password(user_password_form.cleaned_data['new_password'])
                    current_user.save()

                    messages.success(request, 'Parola a fost schimbata cu succes!')
                    return redirect(app)
                else:
                    messages.error(request, 'Parola noua si confirmarea parolei nu sunt identice!')
                    return redirect(app)
            else:
                messages.error(request, 'Parola actuala introdusa este eronata!')
                return redirect(app)
        else:
            messages.error(request, user_password_form.errors)
            return redirect(app)
