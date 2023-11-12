import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from bank_account.comissions import apply_comissions
from bank_account.models import BankAccount
from card.models import Card

from .forms import PaymentForm
from .models import Payment

PAYMENT_KIND = 'PAY'


@csrf_exempt
def payment_curl_proccess(request):
    data = json.loads(request.body)
    business = data.get('business')
    ccc = data.get('ccc')
    pin = data.get('pin')
    amount = float(data.get('amount'))
    try:
        card = Card.active.get(code=ccc)
        if card and check_password(pin, card.pin):
            bank_account = BankAccount.active.get(code=card.bank_account)
            if bank_account and amount <= bank_account.balance:
                bank_account.balance = max(float(bank_account.balance) - amount, 0)
                bank_account.balance = apply_comissions(
                    bank_account.balance,
                    amount,
                    PAYMENT_KIND,
                )
                bank_account.save()
                payment = Payment(
                    business=business,
                    ccc=card,
                    pin=card.pin,
                    amount=amount,
                )
                payment.save()
                return HttpResponse('200 OK\n')
    except BankAccount.DoesNotExist:
        return HttpResponseForbidden('403 Forbidden Bank Account \n')
    except Card.DoesNotExist:
        return HttpResponseForbidden('403 Forbidden Card\n')
    return HttpResponseBadRequest('400 Bad Request\n')


@login_required
def payment_proccess(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            cd = payment_form.cleaned_data
            card = Card.active.get(code=cd['ccc'])
            bank_account = BankAccount.active.get(code=card.bank_account)
            if cd['amount'] <= bank_account.balance:
                bank_account.balance = max(bank_account.balance - cd['amount'], 0)
                bank_account.balance = apply_comissions(
                    bank_account.balance,
                    cd['amount'],
                    PAYMENT_KIND,
                )
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
    payments = Payment.objects.filter(user=request.user)
    return render(
        request,
        'display_payment.html',
        {'section': 'payments', 'payments': payments},
    )


@login_required
def payment_done(request):
    return render(request, 'payment/done.html', {'section': 'payments'})
