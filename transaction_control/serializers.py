from rest_framework import serializers  # type: ignore
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "status",
            "buyer",
            "item",
            "created_at",
        ]
        read_only_fields = ("id", "created_at", "item")
