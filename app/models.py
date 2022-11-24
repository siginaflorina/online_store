from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.

from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'app_category'
    name = models.CharField(max_length=50)

    def __repr__(self):
        return f"Category [name={self.name}]"


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
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=500, null=True)
    preferred_communication_channel = models.CharField(choices=Channels.choices, max_length=10, null=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"User [username={self.username} | email={self.email} | role={self.role.name}]"


class Product(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=True)
    nr_stars = models.IntegerField(null=False, default=0)
    image = models.CharField(max_length=500, null=True)
    price = models.FloatField(null=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @property
    def range_nr_stars_full(self):
        return range(0, self.nr_stars)

    @property
    def range_nr_stars_empty(self):
        return range(0, 5 - self.nr_stars)

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'nr_stars': self.nr_stars,
            'description': self.description,
            'range_nr_stars_full': self.range_nr_stars_full,
            'range_nr_stars_empty': self.range_nr_stars_empty,
            'image': self.image,
            'price': "{:.2f}".format(self.price),
            'category': self.category.name
        }

    def __repr__(self):
        return f"Product [title={self.title}] | [nr_stars={self.nr_stars}] | [image={self.image}] | [price={self.price}] | [description={self.description}]"

    def __str__(self):
        return f"Product [title={self.title}] | [nr_stars={self.nr_stars}] | [image={self.image}] | [price={self.price}] | [description={self.description}]"


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        PROCESSING = 'processing'
        DELIVERING = 'delivering'
        FINISHED = 'finished'

    total_cost = models.FloatField(null=True)
    delivery_address = models.CharField(max_length=500)
    message = models.CharField(max_length=500, null=True)
    date_of_submission = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)

    client = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    def __repr__(self):
        return f"Order [id={self.id}] | " \
               f"[total_cost={self.total_cost}] | " \
               f"[delivery_address={self.delivery_address}] | " \
               f"[message={self.message}] | " \
               f"[date_of_submission={self.date_of_submission}] | " \
               f"status={self.status} | " \
               f"client={self.client.id}"

    def __str__(self):
        return f"Order [id={self.id}] | " \
               f"[total_cost={self.total_cost}] | " \
               f"[delivery_address={self.delivery_address}] | " \
               f"[message={self.message}] | " \
               f"[date_of_submission={self.date_of_submission}] | " \
               f"status={self.status} | " \
               f"client={self.client.id}"


class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_products = models.IntegerField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __repr__(self):
        return f"OrderLine [id={self.id}] | " \
               f"[product={self.product.id}] | " \
               f"[number_of_products={self.number_of_products}] | " \
               f"[order={self.order.id}]"

    def __str__(self):
        return f"OrderLine [id={self.id}] | " \
               f"[product={self.product.id}] | " \
               f"[number_of_products={self.number_of_products}] | " \
               f"[order={self.order.id}]"
