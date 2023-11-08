import re

from django import forms

from .models import Transaction

REGEX = r'A\d-\d{4}'


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['sender', 'cac', 'concept', 'amount']

    def clean_amount(self):
        cd = self.cleaned_data
        return float(cd['amount'])

    def clean_cac(self):
        cd = self.cleaned_data
        if re.match(REGEX, cd['cac']):
            return cd['cac']
        raise forms.ValidationError('Code Account Client error')
