from rest_framework.decorators import api_view, permission_classes  # type: ignore
from rest_framework import status  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from .models import Item, Transaction
from .serializers import TransactionSerializer


User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transaction(request: Request):
    buyer = request.data.get("buyer")  # type: ignore
    seller = request.data.get("seller")  # type: ignore
    item = request.data.get("item")  # type: ignore

    if request.method == "POST":
        buyer_obj = get_object_or_404(User, id=buyer)
        seller_obj = get_object_or_404(User, id=seller)
        item_obj = get_object_or_404(Item, id=item)

        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            transaction_obj = Transaction.objects.create(
                buyer=buyer_obj,
                seller=seller_obj,
                amount=serializer.validated_data.get("amount"),  # type: ignore
                item=item_obj,
                status=serializer.validated_data.get("status"),  # type: ignore
            )
            transaction_obj.save()
            return Response(
                {
                    "success": "Transaction registered successfully",
                    "data": serializer.data,
                    "item": item_obj.name,
                },
                status=status.HTTP_201_CREATED,
            )
