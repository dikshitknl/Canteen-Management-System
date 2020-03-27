from django.db import models

# Create your models here.
MENU_ITEM_CHOICES = [

    (1, "Veg w egg"),
    (2, "Veg w/o egg"),
    (3, "Non-Veg"),

]


class Person(models.Model):
    name = models.CharField(max_length=256, blank=False,
                            null=False, verbose_name="Name ")
    gender = models.SmallIntegerField(choices=[
        (0, "--Select--"),
        (1, "Male"),
        (2, "Female"),
        (3, "Others")
    ], default=0, verbose_name="Gender ")
    phone = models.CharField(
        max_length=15, blank=False, null=False, unique=True, verbose_name="Phone # ")
    designation = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Position ")
    empNum = models.CharField(
        max_length=6, unique=True, verbose_name="Employee ID ")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=200, null=False,
                            blank=False, unique=True, verbose_name="Item Name ")
    price = models.PositiveIntegerField(
        blank=False, null=False, verbose_name="Price (per Plate) ")
    is_available = models.BooleanField(default=True, verbose_name="Available ")
    preparation_time = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Time required to prepare")
    options = models.SmallIntegerField(
        choices=MENU_ITEM_CHOICES, default=2, verbose_name="Food Style ")

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    is_fulfilled = models.BooleanField(
        default=False, verbose_name="Is this Item delivered?")
    time_issued = models.DateTimeField(auto_now_add=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    additional = models.TextField(blank=True)


class Bill(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, primary_key=True)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return "Bill #{} for Order #{}".format(self.bill_no, self.order.id)
