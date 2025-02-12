from django.db import models
from django.db.models import Sum, F


class Item(models.Model):
    name = models.CharField(max_length=256, verbose_name="Name of dish")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")

    def __str__(self):
        return self.name


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "PE", "Pending"
        READY = "RE", "Ready"
        PAID = "PA", "Paid"
    
    class Meta():
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    table_number = models.PositiveSmallIntegerField(verbose_name="Table number")
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )

    items = models.ManyToManyField(Item, through='OrderItem')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total price"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_price(self):
        """Recalculates the total order value and saves it."""
        if self.status in ["RE", "PA"]:
            return # Если заказ завершен - перерасчет не выполняется
        
        total = self.orderitem_set.aggregate(
            total=Sum(F("item__price") * F("quantity"))
        )["total"] or 0
        self.total_price = total
        self.save()
    
    def __str__(self):
        return f"Order {self.id} — Table {self.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    def save(self, *args, **kwargs):
        """Updates the order total price when a dish is added/changed."""
        if self.order.status not in ["RE", "PA"]:
            super().save(*args, **kwargs)
            self.order.update_total_price()
        else:
            raise ValueError("You cannot modify an order with a status of 'Ready' or 'Paid'.")
    
    def delete(self, *args, **kwargs):
        """Updates the order total price when a dish is deleted."""
        if self.order.status not in ["RE", "PA"]:
            super().delete(*args, **kwargs)
            self.order.update_total_price()
        else:
            raise ValueError("You cannot modify an order with a status of 'Ready' or 'Paid'.")
    
    def __str__(self):
        return f"{self.quantity} x {self.item.price} for order {self.order.id}"

