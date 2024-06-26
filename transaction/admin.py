from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['cac', 'sender', 'timeStamp', 'amount', 'kind']
    list_filter = [
        'timeStamp',
        'kind',
    ]
    ordering = ['-timeStamp']
