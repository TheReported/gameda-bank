from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'cac', 'timeStamp', 'amount', 'kind']
    raw_id_fields = ['sender']
    list_filter = [
        'timeStamp',
        'kind',
    ]
    ordering = ['-timeStamp']
