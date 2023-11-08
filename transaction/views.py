from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from bank_account.models import BankAccount

from .forms import TransactionForm
from .models import Transaction


def transaction_outgoing_proccess(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            cd = transaction_form.cleaned_data
            amount = float(cd['amount'])
            bank_account = get_object_or_404(BankAccount, id=cd['cac'])
            if bank_account and amount <= bank_account.balance:
                ...

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


@login_required
def transaction_inconming_proccess(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            cd = transaction_form.cleaned_data
            bank_account = get_object_or_404(BankAccount, id=cd['cac'])
            if bank_account:
                ...
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


@login_required
def display_transaction(request):
    transactions = Transaction.objects.all()
    return render(
        request, 'display_payment.html', {'section': 'transactions', 'transactions': transactions}
    )


@login_required
def transaction_done(request):
    return render(request, 'transaction/done.html', {'section': 'transactions'})
