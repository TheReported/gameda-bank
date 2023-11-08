import re

from django import forms

from .models import Transaction

REGEX = r'A\d-\d{4}'


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['bank_account', 'agent', 'concept', 'amount']

    def clean_agent(self):
        cd = self.cleaned_data
        if re.match(REGEX, cd['agent']):
            return cd['agent']
        raise forms.ValidationError('Agent code error')
