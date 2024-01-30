import csv
import datetime

from django.db import models
from django.http import HttpResponse

COMISSIONS = {
    "OUT": {"Tier1": 2, "Tier2": 4, "Tier3": 6},
    "INC": {"Tier1": 1, "Tier2": 2, "Tier3": 3},
    "PAY": {"Tier1": 3, "Tier2": 5, "Tier3": 7},
}


class MovementKind(models.TextChoices):
    OUTGOING = 'OUT', 'Outgoing'
    INCOMING = 'INC', 'Incoming'
    PAYMENT = 'PAY', 'Payment'


def apply_movement(acc, transaction):
    if acc.balance >= (total_amount := transaction.amount + transaction.commission):
        acc.balance -= total_amount
        return acc, True
    return acc, False


def export_to_csv(request, queryset):
    opts = queryset.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [
        field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
