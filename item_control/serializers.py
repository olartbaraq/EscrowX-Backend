from rest_framework import serializers  # type: ignore
from .models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ["name", "description", "price"]
        read_only_fields = ("id",)
