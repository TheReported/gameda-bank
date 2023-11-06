from django import forms
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

from bank_account.models import BankAccount
from card.models import Card

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['business', 'ccc', 'pin', 'amount']

    def clean_pin(self):
        cd = self.cleaned_data
        amount = int(cd['amount'])
        card = get_object_or_404(Card, ccc=cd['ccc'])
        if card and check_password(cd['pin'], card.pin):
            bank_account = get_object_or_404(BankAccount, code=card.bank_account)
            if amount <= bank_account.balance:
                bank_account.balance = max(bank_account.balance - amount, 0)
                bank_account.save()
            else:
                raise forms.ValidationError(
                    f'The card associated with the account {bank_account.code} \
                    does not have enough money'
                )
        else:
            raise forms.ValidationError('The inserted card data is not correct')
