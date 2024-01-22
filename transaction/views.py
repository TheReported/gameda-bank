import json
from decimal import Decimal

import requests
import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.utils import Status, get_info_bank
from bank_account.models import BankAccount
from bank_account.utils import apply_movement, export_to_csv

from .forms import TransactionForm
from .models import Transaction


@login_required
def transaction_outgoing_proccess(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            cd = transaction_form.cleaned_data
            cac = cd['cac']
            amount = Decimal(cd['amount'])
            sender = get_object_or_404(
                BankAccount, code=cd['sender'], user=request.user, status=Status.ACTIVE
            )

            cac = (
                get_object_or_404(BankAccount, code=cd['cac'], status=Status.ACTIVE)
                if cac[:2] == 'A7'
                else False
            )
            if sender == cac:
                return HttpResponseBadRequest('Sender and cac are equal')

            if sender and cac:
                if amount <= sender.balance:
                    transaction = transaction_form.save(commit=False)
                    sender.balance, status_movement = apply_movement(
                        sender.balance, amount, transaction.kind
                    )
                    if status_movement:
                        cac.balance += amount
                        transaction.user = request.user
                        sender.save()
                        cac.save()
                        transaction.save()
                        messages.success(request, "Your payment has been done successfully")
                        return redirect('transaction:done')
                    else:
                        messages.error(request, 'You dont have enough money')
            else:
                bank = get_info_bank(cd['cac'])
                response = requests.post(
                    f'{bank["url"]}:8000/transfer/incoming/', json=request.POST
                )
                if response.status_code == 200:
                    transaction = transaction_form.save(commit=False)
                    sender.balance, status_movement = apply_movement(
                        sender.balance, cd['amount'], transaction.kind
                    )
                    if status_movement:
                        sender.save()
                        transaction.save()
                        messages.success(request, "Your payment has been done successfully")
                        return redirect('transaction:done')
                return HttpResponseBadRequest()
        else:
            messages.error(request, "There was an error on your transaction")
    else:
        transaction_form = TransactionForm()
    return render(
        request,
        'transaction/created.html',
        {
            'section': 'transactions',
            'transaction_form': transaction_form,
        },
    )


@require_POST
@csrf_exempt
def transaction_inconming_proccess(request):
    data = json.loads(request.body)
    amount = Decimal(data['amount'])
    try:
        bank_account = BankAccount.active.get(code=data['cac'])
    except BankAccount.DoesNotExist:
        return HttpResponseForbidden('Bank account does not exists')

    bank_account.balance += amount
    bank_account.save()
    transaction = Transaction(
        sender=data['sender'],
        cac=bank_account,
        concept=data['concept'],
        amount=amount,
        kind=Transaction.Kind.INCOMING,
    )
    transaction.save()
    return HttpResponse()


@login_required
def display_transaction(request):
    bank_accounts = BankAccount.active.filter(user=request.user)
    all_transactions = []

    for bank_account in bank_accounts:
        transaction = Transaction.objects.filter(
            Q(sender=bank_account.code) | Q(cac=bank_account.code)
        )
        all_transactions.extend(transaction)

    paginator = Paginator(all_transactions, 10)
    page = request.GET.get("page")

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    return render(
        request,
        'display_transaction.html',
        {'section': 'transactions', 'transactions': transactions},
    )


@login_required
def transaction_done(request):
    return render(request, 'transaction/done.html', {'section': 'transactions'})


def transaction_pdf(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    html = render_to_string('transaction/pdf.html', {'transaction': transaction})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=transaction_{transaction.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    )
    return response


def transaction_csv(request, transaction_id):
    response = export_to_csv(request, queryset=Transaction.objects.filter(id=transaction_id))

    return response


def all_transaction_csv(request):
    response = export_to_csv(request, Transaction.objects.filter(cac=request.user.id))

    return response
