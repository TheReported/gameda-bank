import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from bank_account.comissions import apply_comissions
from bank_account.models import BankAccount

from .forms import TransactionForm
from .models import Transaction


@login_required
def transaction_outgoing_proccess(request):
    if request.method == 'POST':
        if request.POST.get('sender') == request.POST.get('cac'):
            return HttpResponseBadRequest('Sender and cac are equals')
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            cd = transaction_form.cleaned_data
            amount = cd['amount']
            try:
                sender = BankAccount.active.get(code=cd['sender'], user=request.user)
                cac = BankAccount.active.get(code=cd['cac'])
            except BankAccount.DoesNotExist:
                return HttpResponseBadRequest('Matraca')
            if amount <= sender.balance:
                transaction = transaction_form.save(commit=False)
                sender.balance -= amount
                sender.balance = apply_comissions(sender.balance, cd['amount'], transaction.kind)
                cac.balance += amount
                transaction.user = request.user
                sender.save()
                cac.save()
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
def transaction_inconming_proccess(request):
    data = json.loads(request.body)
    amount = float(data['amount'])
    try:
        bank_account = BankAccount.active.get(id=data['cac'])
        bank_account.balance += amount
        bank_account.balance = apply_comissions(
            bank_account.balance, amount, Transaction.Kind.INCOMING
        )
        bank_account.save()
        transaction = Transaction(
            sender=data['sender'],
            cac=bank_account,
            concept=data['sender'],
            amount=amount,
            kind=Transaction.Kind.INCOMING,
        )
        transaction.save()
        return HttpResponse({'status': 'ok'})
    except BankAccount.DoesNotExist:
        return HttpResponseForbidden('Bank account does not exists')

    return HttpResponseBadRequest('The data you have sent is incorrect')


@login_required
def display_transaction(request):
    all_transactions = {}
    bank_accounts = BankAccount.active.filter(user=request.user)
    for bank_account in bank_accounts:
        try:
            transactions = Transaction.objects.filter(
                sender=bank_account.code
            ) | Transaction.objects.filter(cac=bank_account.code)
            for transaction in transactions:
                if all_transactions.get(bank_account):
                    all_transactions[bank_account].append(transaction)
                else:
                    all_transactions[bank_account] = [transaction]
        except Transaction.DoesNotExist:
            continue
    transactions = [
        transaction
        for _, all_transactions in all_transactions.items()
        for transaction in all_transactions
    ]
    return render(
        request,
        'display_transaction.html',
        {'section': 'transactions', 'transactions': transactions},
    )


@login_required
def transaction_done(request):
    return render(request, 'transaction/done.html', {'section': 'transactions'})
