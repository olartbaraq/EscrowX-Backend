from django.contrib import admin  # type: ignore

from transaction_control.models import Transaction  # type: ignore

# Register your models here.


admin.site.register(Transaction)
