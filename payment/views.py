from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, redirect, render

from bank_account.comissions import apply_comissions
from bank_account.models import BankAccount
from card.models import Card

from .forms import PaymentForm
from .models import Payment


@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            cd = payment_form.cleaned_data
            amount = float(cd['amount'])
            card = get_object_or_404(Card, code=cd['ccc'])
            if card and check_password(cd['pin'], card.pin):
                bank_account = get_object_or_404(BankAccount, code=card.bank_account)
                if amount <= bank_account.balance:
                    bank_account.balance = max(float(bank_account.balance) - amount, 0)
                    bank_account.balance = apply_comissions(bank_account.balance, amount, "PA")
                    bank_account.save()
                    payment_form.save()
                    messages.success(request, "Your payment has been done successfully")
                    return redirect('payment:done')

                messages.error(request, "There was an error on your payment")
    else:
        payment_form = PaymentForm()
    return render(
        request,
        'payment/created.html',
        {
            'section': 'payments',
            'payment_form': payment_form,
        },
    )


@login_required
def display_payment(request):
    payments = Payment.objects.all()
    return render(request, 'display_payment.html', {'section': 'payments', 'payments': payments})


@login_required
def payment_done(request):
    return render(request, 'payment/done.html', {'section': 'payments'})
