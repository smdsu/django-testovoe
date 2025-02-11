from django.db import models
from django.db.models import Sum, F


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "PE", "Pending"
        READY = "RE", "Ready"
        PAID = "PA", "Paid"

    table_number = models.PositiveSmallIntegerField(verbose_name="Table number")
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total price"
    )

    def update_total_price(self):
        """Recalculates the total order value and saves it."""
        total = self.items.aggregate(total=Sum(F("price") * F("quantity")))["total"] or 0
        self.total_price = total
        self.save()
    
    def __str__(self):
        return f"Order {self.id}, (Table {self.table_number})"


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=256, verbose_name="Name of dish")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    def save(self, *args, **kwargs):
        """Updates the order total price when a dish is added/changed."""
        super().save(*args, **kwargs)
        self.order.update_total_price()
    
    def delete(self, *args, **kwargs):
        """Updates the order total price when a dish is deleted."""
        super().delete(*args, **kwargs)
        self.order.update_total_price()
    
    def __str__(self):
        return f"{self.name} x {self.quantity}"

