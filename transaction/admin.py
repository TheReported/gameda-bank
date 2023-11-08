from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['bank_account', 'agent', 'timeStamp', 'amount', 'kind']
    raw_id_fields = ['bank_account']
    list_filter = [
        'timeStamp',
        'kind',
    ]
    ordering = ['-timeStamp']
