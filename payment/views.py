import json
from decimal import Decimal

import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from account.utils import Status
from bank_account.models import BankAccount
from bank_account.utils import MovementKind, apply_movement, export_to_csv
from card.models import Card

from .forms import PaymentForm
from .models import Payment


@csrf_exempt
def payment_curl_proccess(request):
    data = json.loads(request.body)
    amount = Decimal(data.get('amount'))
    try:
        card = Card.active.get(code=data['ccc'])
        if card and check_password(data['pin'], card.pin):
            card.bank_account.balance, status = apply_movement(
                card.bank_account.balance,
                amount,
                MovementKind.PAYMENT,
            )
            if status:
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
            amount = Decimal(cd['amount'])
            card = get_object_or_404(Card, code=cd['ccc'], status=Status.ACTIVE)
            if check_password(cd['pin'], card.pin):
                bank_account = get_object_or_404(
                    BankAccount, code=card.bank_account, status=Status.ACTIVE
                )

                bank_account.balance, status_movement = apply_movement(
                    bank_account.balance, amount, MovementKind.PAYMENT
                )
                if status_movement:
                    bank_account.save()
                    payment = payment_form.save(commit=False)
                    payment.ccc = card
                    payment.save()
                    messages.success(request, "Your payment has been done successfully")
                    return redirect('payment:done')
                else:
                    messages.error(request, f"{bank_account.code} does not have enough money.")
            else:
                messages.error(request, "The pin introduced is not correct")
        else:
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


def payment_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    html = render_to_string('payment/pdf.html', {'payment': payment})
    response = HttpResponse(content_type='payment/pdf')
    response['Content-Disposition'] = f'filename=payment_{payment.id}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[weasyprint.CSS('account/static/css/pdf.css')]
    )
    return response


def payment_csv(request, payment_id):
    response = export_to_csv(request, queryset=Payment.objects.filter(id=payment_id))

    return response


def all_payment_csv(request):
    response = export_to_csv(
        request, queryset=Payment.objects.filter(ccc__bank_account__user=request.user)
    )

    return response
