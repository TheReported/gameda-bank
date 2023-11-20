from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['bank_account', 'alias', 'status', 'code']
    raw_id_fields = ['bank_account']
