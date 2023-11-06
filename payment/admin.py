from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['ccc', 'business', 'amount']
    raw_id_fields = ['ccc']
