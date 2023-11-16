import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from account.utils import Status
from bank_account.comissions import apply_comissions
from bank_account.models import BankAccount
from card.models import Card

from .forms import PaymentForm
from .models import Payment

PAYMENT_KIND = 'PAY'


@csrf_exempt
def payment_curl_proccess(request):
    data = json.loads(request.body)
    amount = float(data.get('amount'))
    try:
        card = Card.active.get(code=data['ccc'])
        if card and check_password(data['pin'], card.pin):
            if amount <= card.bank_account.balance:
                card.bank_account.balance = max(float(card.bank_account.balance) - amount, 0)
                card.bank_account.balance = apply_comissions(
                    card.bank_account.balance,
                    amount,
                    PAYMENT_KIND,
                )
                card.bank_account.save()
                payment = Payment(
                    business=data['business'],
                    ccc=card,
                    pin=card.pin,
                    amount=amount,
                )
                payment.save()
                return HttpResponse('200 OK\n')
    except Card.DoesNotExist:
        return HttpResponseForbidden('403 Forbidden Card\n')
    return HttpResponseBadRequest('400 Bad Request\n')


@login_required
def payment_proccess(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            cd = payment_form.cleaned_data
            card = get_object_or_404(Card, code=cd['ccc'], status=Status.ACTIVE)
            if check_password(cd['pin'], card.pin):
                bank_account = get_object_or_404(
                    BankAccount, code=card.bank_account, status=Status.ACTIVE
                )
                if cd['amount'] <= bank_account.balance:
                    bank_account.balance = max(bank_account.balance - cd['amount'], 0)
                    bank_account.balance = apply_comissions(
                        bank_account.balance, cd['amount'], PAYMENT_KIND
                    )
                    bank_account.save()
                    payment = payment_form.save(commit=False)
                    payment.ccc = card
                    payment.save()
                    messages.success(request, "Your payment has been done successfully")
                    return redirect('payment:done')
                messages.error(request, f"{bank_account.code} does not have enough money.")
            messages.error(request, "The pin introduced is not correct")
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
    all_payments = Payment.objects.filter(ccc__bank_account__user=request.user)
    paginator = Paginator(all_payments, 10)
    page = request.GET.get("page")

    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)
    return render(
        request,
        'display_payment.html',
        {'section': 'payments', 'payments': payments},
    )


@login_required
def payment_done(request):
    return render(request, 'payment/done.html', {'section': 'payments'})
