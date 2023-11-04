from django.contrib import admin

from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'alias', 'balance', 'status', 'code']
    raw_id_fields = ['user']
