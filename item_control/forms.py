from django.forms import ModelForm  # type: ignore
from cloudinary.forms import CloudinaryFileField  # type: ignore
from .models import Item


class PhotoForm(ModelForm):
    image = CloudinaryFileField

    class Meta:
        model = Item
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].options = {
            "tags": "new_image",
            "format": "png",
        }
