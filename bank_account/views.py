from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import BankAccountForm
from .models import BankAccount


@login_required
def display(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(
        request,
        'display_bank.html',
        {'accounts': accounts},
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
        else:
            messages.error(request, 'Error creating a bank account')
    else:
        bank_account_form = BankAccountForm()
    return render(
        request,
        'bank_account/create.html',
        {'bank_account_form': bank_account_form},
    )
