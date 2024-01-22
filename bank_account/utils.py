import csv
import datetime

from django.http import HttpResponse

COMISSIONS = {
    "OUT": {"Tier1": 2, "Tier2": 4, "Tier3": 6},
    "INC": {"Tier1": 1, "Tier2": 2, "Tier3": 3},
    "PAY": {"Tier1": 3, "Tier2": 5, "Tier3": 7},
}


def apply_movement(acc_balance, amount, kind):
    if kind in COMISSIONS:
        if 0 <= amount < 50:
            total_amount = amount + (amount * COMISSIONS[kind]["Tier1"] / 100)
        elif 50 <= amount < 500:
            total_amount = amount + (amount * COMISSIONS[kind]["Tier2"] / 100)
        elif amount >= 500:
            total_amount = amount + (amount * COMISSIONS[kind]["Tier3"] / 100)

        if acc_balance >= total_amount:
            total_balance = acc_balance - total_amount
            return total_balance, True
    return acc_balance, False


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
