from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from account.utils import Status
from card.models import Card
from transaction.models import Transaction

from .forms import BankAccountEditForm, BankAccountForm
from .models import BankAccount


@login_required
def display(request):
    bank_accounts = BankAccount.active.filter(user=request.user)
    return render(
        request,
        'display_bank_account.html',
        {'section': 'accounts', 'accounts': bank_accounts},
    )


@login_required
def create(request):
    if request.method == 'POST':
        bank_account_form = BankAccountForm(request.POST)
        if bank_account_form.is_valid():
            bank_account = bank_account_form.save(commit=False)
            bank_account.user = request.user
            bank_account.save()

            messages.success(request, 'Create a bank account successfully')
            return redirect('bank_account:display')

        else:
            messages.error(request, 'Error creating a bank account')
    else:
        bank_account_form = BankAccountForm()
    return render(
        request,
        'bank_account/create.html',
        {'section': 'accounts', 'bank_account_form': bank_account_form},
    )


@login_required
def create_done(request):
    return render(
        request,
        'bank_account/done.html',
        {'section': 'accounts'},
    )


@login_required
def detail(request, code):
    bank_account = get_object_or_404(BankAccount, code=code, status=Status.ACTIVE)
    cards = Card.active.filter(bank_account=bank_account)
    transactions = Transaction.objects.filter(sender=code) | Transaction.objects.filter(
        cac__code=code
    )

    if bank_account:
        return render(
            request,
            'bank_account/detail.html',
            {
                'section': 'accounts',
                'bank_account': bank_account,
                'cards': cards,
                'transactions': transactions,
            },
        )


@login_required
def edit(request, code):
    bank_account = get_object_or_404(BankAccount, code=code, status=Status.ACTIVE)
    if request.method == 'POST':
        bank_account_form = BankAccountEditForm(instance=bank_account, data=request.POST)
        if bank_account_form.is_valid():
            bank_account_form.save()
            messages.success(request, 'Edit a bank account successfully')
            return redirect(bank_account.get_absolute_url())
        else:
            messages.error(request, 'Error editing a bank account')
    else:
        bank_account_form = BankAccountEditForm(instance=bank_account)
    return render(
        request,
        'bank_account/edit.html',
        {
            'section': 'accounts',
            'bank_account_edit_form': bank_account_form,
            'bank_account': bank_account,
        },
    )


@login_required
@require_POST
def discharge(request, code):
    bank_account = get_object_or_404(BankAccount, code=code, status=Status.ACTIVE)
    bank_account.status = Status.DISCHARGE
    bank_account.save()
    messages.success(request, 'You have discharge your bank account successfully')
    return redirect('bank_account:display')
