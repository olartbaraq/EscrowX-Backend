from rest_framework.decorators import api_view, permission_classes  # type: ignore
from rest_framework import status  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from .models import Item
from .serializers import ItemSerializer
from .forms import PhotoForm


User = get_user_model()

# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_item(request: Request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        user = request.user
        serializer = ItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if form.is_valid():
                item_obj = Item.objects.create(
                    name=serializer.validated_data["name"],  # type: ignore
                    description=serializer.validated_data["description"],  # type: ignore
                    price=serializer.validated_data["price"],  # type: ignore
                    seller=user,
                )
                item_obj.save()
                form.save()
                return Response(
                    {
                        "success": "Item registered successfully",
                        "data": serializer.data,
                        "seller": user.name,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
