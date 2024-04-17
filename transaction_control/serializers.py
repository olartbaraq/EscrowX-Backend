from rest_framework import serializers  # type: ignore
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [""]
        read_only_fields = ("id",)
