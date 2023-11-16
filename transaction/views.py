import json

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.utils import Status, get_info_bank
from bank_account.comissions import apply_comissions
from bank_account.models import BankAccount

from .forms import TransactionForm
from .models import Transaction


@login_required
def transaction_outgoing_proccess(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            cd = transaction_form.cleaned_data
            cac = cd['cac']
            amount = cd['amount']
            sender = get_object_or_404(
                BankAccount, code=cd['sender'], user=request.user, status=Status.ACTIVE
            )

            if sender == cac:
                return HttpResponseBadRequest('Sender and cac are equal')

            if sender and cac:
                if amount <= sender.balance:
                    transaction = transaction_form.save(commit=False)
                    sender.balance -= amount
                    sender.balance = apply_comissions(
                        sender.balance, cd['amount'], transaction.kind
                    )
                    cac.balance += amount
                    transaction.user = request.user
                    sender.save()
                    cac.save()
                    transaction.save()
                    messages.success(request, "Your payment has been done successfully")
                    return redirect('transaction:done')
            else:
                bank = get_info_bank(cac.code)
                response = requests.post(f'{bank["url"]}/transaction/incoming', data=request.POST)
                if response.status_code == 200:
                    if amount <= sender.balance:
                        transaction = transaction_form.save(commit=False)
                        sender.balance -= amount
                        sender.balance = apply_comissions(
                            sender.balance, cd['amount'], transaction.kind
                        )
                        sender.save()
                        transaction.save()
                        messages.success(request, "Your payment has been done successfully")
                    return redirect('transaction:done')

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
    amount = float(data['amount'])
    try:
        bank_account = BankAccount.active.get(code=data['cac'])
    except BankAccount.DoesNotExist:
        return HttpResponseForbidden('Bank account does not exists')

    bank_account.balance = float(bank_account.balance) + amount
    bank_account.balance = apply_comissions(bank_account.balance, amount, Transaction.Kind.INCOMING)
    bank_account.save()
    transaction = Transaction(
        sender=data['sender'],
        cac=bank_account,
        concept=data['sender'],
        amount=amount,
        kind=Transaction.Kind.INCOMING,
    )
    transaction.save()
    return HttpResponse()


@login_required
def display_transaction(request):
    bank_accounts = BankAccount.active.filter(user=request.user)
    transactions = []

    for bank_account in bank_accounts:
        transaction = Transaction.objects.filter(Q(sender=bank_account.code) | Q(cac=bank_account))
        transactions.extend(transaction)

    return render(
        request,
        'display_transaction.html',
        {'section': 'transactions', 'transactions': transactions},
    )


@login_required
def transaction_done(request):
    return render(request, 'transaction/done.html', {'section': 'transactions'})
