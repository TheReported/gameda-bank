from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['user', 'alias', 'status', 'code', 'pin']
    raw_id_fields = ['user']
