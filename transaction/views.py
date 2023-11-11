import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

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
            amount = cd['amount']
            sender = BankAccount.active.get(code=cd['sender'])
            cac = BankAccount.active.get(code=cd['cac'])
            if amount <= sender.balance:
                transaction = transaction_form.save(commit=False)
                sender.balance -= amount
                sender.balance = apply_comissions(sender.balance, cd['amount'], transaction.kind)
                cac.balance += amount
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
            'sender': sender,
        },
    )


@require_POST
def transaction_inconming_proccess(request):
    data = json.loads(request.body)
    amount = float(data['amount'])
    try:
        bank_account = BankAccount.active.get(id=data['cac'])
        bank_account.balance += amount
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
        return HttpResponseBadRequest('Bank account does not exists')

    return HttpResponseBadRequest('The data you have sent is incorrect')


@login_required
def display_transaction(request):
    transactions = Transaction.objects.all()
    return render(
        request,
        'display_transaction.html',
        {'section': 'transactions', 'transactions': transactions},
    )


@login_required
def transaction_done(request):
    return render(request, 'transaction/done.html', {'section': 'transactions'})
