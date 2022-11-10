from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.

from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'app_category'
    name = models.CharField(max_length=50)


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    # cand se va sterge o categorie, se va sterge automat toate subcategoriile ce fac parte din categoria "mama"
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Role(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __repr__(self):
        return f"Role [name={self.name}]"

    def __str__(self):
        return f"Role [name={self.name}]"


class User(AuthUser):
    class Channels(models.TextChoices):
        MAIL = "mail"
        EMAIL = "email"

    USERNAME_FIELD = "email"
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=500, null=True)
    profile_img = models.CharField(max_length=500, null=True)
    preferred_communication_channel = models.CharField(choices=Channels.choices, max_length=10, null=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"User [name={self.email} | role={self.role.name} | password={self.password}]"


class Product(models.Model):
    class ProductType(models.TextChoices):
        pass

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    thumbnail = models.CharField(max_length=500)
    price = models.FloatField()
    product_type = models.CharField(choices=ProductType.choices, max_length=30)

    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        PROCESSING = 'processing'
        DELIVERING = 'delivering'
        FINISHED = 'finished'

    total_cost = models.FloatField()
    delivery_address = models.CharField(max_length=500)
    date_of_submission = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=Status.choices, max_length=20)

    client = models.ForeignKey(User, on_delete=models.CASCADE)


class Cart(models.Model):
    pass


class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_products = models.IntegerField()
    product_price = models.FloatField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

