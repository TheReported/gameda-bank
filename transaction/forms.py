import re

from django import forms

from .models import Transaction

REGEX = r'A\d-\d{4}'


class TransactionForm(forms.ModelForm):
    cac = forms.CharField(max_length=7)

    class Meta:
        model = Transaction
        fields = ['sender', 'cac', 'concept', 'amount']

    def clean_sender(self):
        cd = self.cleaned_data
        if re.match(REGEX, cd['sender']):
            return cd['sender']
        raise forms.ValidationError('Sender error')
