from django import template

from payment.models import Payment

register = template.Library()


@register.simple_tag
def show_latest_payments(user, count=5):
    return Payment.objects.filter(ccc__bank_account__user=user.id)[:count]
