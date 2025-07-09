from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class ApiUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('provider', 'Поставщик'),
        ('consumer', 'Потребитель'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES, default='provider'
    )

    

class Warehouse(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"WH ID {self.id}: {self.name}"
    

class Good(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"Goods ID {self.id}: {self.name}"
    

class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name="goods", on_delete=models.CASCADE)
    good = models.ForeignKey(Good, related_name="warehouses", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  # количество товара

    def add_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")
        self.quantity += quantity
        self.save()

    def remove_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")
        if self.quantity < quantity:
            raise ValueError("Недостаточно товара на складе")
        self.quantity -= quantity
        self.save()

    class Meta:
        unique_together = ('warehouse', 'good')

    def __str__(self):
        return f"On {self.warehouse.name} warehouse exist {self.quantity} items of {self.good.name}"
    

    

