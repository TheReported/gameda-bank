from django import forms

from .models import BankAccount


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['alias']


class BankAccountEditForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['alias']
