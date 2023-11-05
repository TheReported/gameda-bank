from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from bank_account.models import BankAccount
from card.models import Card

from .models import Payment


@require_POST
def process_payment(request):
    business = request.POST.get('business')
    ccc = request.POST.get('ccc')
    pin = request.POST.get('pin')
    amount = request.POST.get('amount')
    card = get_object_or_404(Card, code='ccc')
    if card:
        bank_account = get_object_or_404(BankAccount, bank_account=card.bank_account)
        payment_amount = int(amount)
        bank_account_balance = int(bank_account.balance)
        if payment_amount <= bank_account_balance:
            new_balance = max(bank_account_balance - payment_amount, 0)
            bank_account.balance = new_balance
            bank_account.save()
            payment = Payment(business=business, ccc=ccc, pin=pin, amount=amount)
            payment.save()
        else:
            messages.error('You dont have enough money')


@login_required
def display_payment(request):
    payments = Payment.objects.all()
    return render(request, 'display_payment.html', {'section': 'payment', 'payments': payments})
