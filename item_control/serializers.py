from rest_framework import serializers  # type: ignore
from .models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "image",
            "price",
            "created_at",
        ]
        read_only_fields = ("id", "created_at", "image", "seller")
