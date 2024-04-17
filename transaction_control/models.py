from django.db import models  # type: ignore

from user_control.models import User
from item_control.models import Item

# Create your models here.

status = (
    ("Pending", "Pending"),
    ("Cancelled", "Cancelled"),
    ("Completed", "Completed"),
)


class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    amount = models.FloatField(blank=False, null=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
    status = models.CharField(max_length=10, choices=status, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer.name} - {self.seller.name}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Transaction"
