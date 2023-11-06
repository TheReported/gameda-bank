from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import PaymentForm
from .models import Payment

# and card and check_password(pin, card.pin)


@require_POST
def process_payment(request):
    payment_form = PaymentForm(request.POST)
    if payment_form.is_valid():
        payment_form.save()
        messages.success('All right!')

    else:
        messages.error('Card error')
    return render(
        request,
        'bank_account/created.html',
        {
            'section': 'payment',
            'payment_form': payment_form,
        },
    )


@login_required
def display_payment(request):
    payments = Payment.objects.all()
    return render(request, 'display_payment.html', {'section': 'payment', 'payments': payments})
