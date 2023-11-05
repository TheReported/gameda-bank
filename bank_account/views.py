from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from account.status import ACTIVE
from card.models import Card

from .forms import BankAccountForm
from .models import BankAccount


@login_required
def display(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(
        request,
        'display_bank_account.html',
        {'section': 'accounts', 'accounts': accounts},
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
            return redirect('bank_account:create_done')

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
def detail(request, id):
    bank_account = get_object_or_404(BankAccount, id=id, status=ACTIVE)
    if bank_account:
        cards = Card.objects.filter(bank_account=bank_account)
        return render(
            request,
            'bank_account/detail.html',
            {'section': 'accounts', 'bank_account': bank_account, 'cards': cards},
        )
