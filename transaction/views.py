from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bank_account.models import BankAccount

from .forms import TransactionForm
from .models import Transaction


@login_required
def transaction_outgoing_proccess(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            cd = transaction_form.cleaned_data
            bank_account = BankAccount.objects.get(id=cd['sender'])
            if cd['amount'] <= bank_account.balance:
                bank_account.balance -= cd['amount']
                bank_account.save()
                transaction_form.save()

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
    transaction_form = TransactionForm(request.POST)
    if transaction_form.is_valid():
        cd = transaction_form.cleaned_data
        try:
            bank_account = BankAccount.objects.get(id=cd['cac'])
            bank_account.balance += cd['amount']
            bank_account.save()
            transaction_form.save()
            return HttpResponse(headers={'status': 'ok'})
        except BankAccount.DoesNotExist:
            return HttpResponseBadRequest('Bank account does not exists')
    return HttpResponseBadRequest('The data you have sent is incorrect')


@login_required
def display_transaction(request):
    transactions = Transaction.objects.all()
    return render(
        request, 'display_payment.html', {'section': 'transactions', 'transactions': transactions}
    )


@login_required
def transaction_done(request):
    return render(request, 'transaction/done.html', {'section': 'transactions'})
