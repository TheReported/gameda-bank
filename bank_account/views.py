from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import BankAccountForm
from .models import BankAccount


@login_required
def display_bank_account(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(
        request,
        'bank_account/list.html',
        {'accounts': accounts},
    )


@login_required
def create_bank_account(request):
    accounts = BankAccount.objects.filter(user=request.user)
    if request.method == 'POST':
        bank_account_form = BankAccountForm(request.POST)
        if bank_account_form.is_valid():
            bank_account_form.save()
            messages.success(request, 'Create a bank account successfully')
        else:
            messages.error(request, 'Error creating a bank account')
    else:
        bank_account_form = BankAccountForm()
    return render(
        request,
        'dashboard.html',
        {'bank_account_form': bank_account_form, 'accounts': accounts},
    )
