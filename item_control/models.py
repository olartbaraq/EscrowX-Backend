from django.db import models  # type: ignore
from user_control.models import User
from cloudinary.models import CloudinaryField  # type: ignore

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=1000)
    image = CloudinaryField("image")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_id")
    price = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seller.name} - {self.name}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Item"
