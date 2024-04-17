from django.contrib import admin  # type: ignore
from .models import Item

# Register your models here.

admin.site.register(Item)
