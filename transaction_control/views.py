from rest_framework.decorators import api_view, permission_classes  # type: ignore
from rest_framework import status  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from item_control.serializers import ItemSerializer  # type: ignore
from .models import Item, Transaction
from .serializers import TransactionSerializer
from django.core.mail import EmailMultiAlternatives  # type: ignore
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags  # type: ignore
from django.db import models  # type: ignore
import threading

User = get_user_model()


def send_mail_to_buyer(
    subject: str,
    from_email: str | None,
    seller: str,
    buyer: str,
    item: str,
    recipient_list: list[str],
):
    html_message = render_to_string(
        "content/email.html", context={"seller": seller, "buyer": buyer, "item": item}
    )
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=from_email,
        to=recipient_list,
    )

    message.attach_alternative(html_message, "text/html")
    message.send()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transaction(request: Request):
    buyer = request.data.get("buyer")  # type: ignore
    item = request.data.get("item")  # type: ignore

    if request.method == "POST":
        buyer_obj = get_object_or_404(User, id=buyer)
        item_obj = get_object_or_404(Item, id=item)

        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            transaction_obj = Transaction.objects.create(
                buyer=buyer_obj,
                seller=request.user,
                amount=serializer.validated_data.get("amount"),  # type: ignore
                item=item_obj,
                status=serializer.validated_data.get("status"),  # type: ignore
            )
            transaction_obj.save()

            # Send email notification to buyer

            subject = "Transaction Notification Confirmation!!!"
            # message = f"Hi, {buyer_obj.name}, {request.user.name} have successfully initiated a transaction with you for the item {item_obj.name}. Kindly proceed to make payments."  # type: ignore
            from_email = None
            recipient_list = [
                buyer_obj.email,  # type: ignore
            ]
            seller = request.user.name
            buyer = buyer_obj.name  # type: ignore
            item = item_obj.name

            # Create a new thread to send the email
            email_thread = threading.Thread(
                target=send_mail_to_buyer,
                args=(subject, from_email, seller, buyer, item, recipient_list),
            )
            email_thread.start()

            return Response(
                {
                    "success": "Transaction registered successfully",
                    "data": {
                        "item": item_obj.name,
                        "seller": request.user.name,
                        "buyer": buyer_obj.name,  # type: ignore
                        "amount": serializer.data.get("amount"),  # type: ignore
                        "status": serializer.data.get("status"),  # type: ignore
                    },
                },
                status=status.HTTP_201_CREATED,
            )


# write the view to get all transaction based on the user id
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_transaction_by_id(request: Request):
    seller = request.user

    transaction_logs_by_id = Transaction.objects.filter(
        (models.Q(seller=seller) | models.Q(buyer=seller))
    ).order_by("-created_at")
    serializer = TransactionSerializer(transaction_logs_by_id, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# 3) Get an item by id
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_item_by_id(request: Request, id: int):
    print(id)
    item_obj = Item.objects.get(id=id)
    serializer = ItemSerializer(item_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Todo
# 1) after payment add an update request frpm buyer to change status to Processing
# 2) after delivery add an update request to change status to Completed
