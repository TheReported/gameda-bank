from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['bank_account', 'user', 'alias', 'status', 'code', 'get_pin', 'pin']
    raw_id_fields = ['bank_account', 'user']
