from django import forms

from account.utils import Status

from .models import BankAccount, Transaction


class TransactionForm(forms.ModelForm):
    sender = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Transaction
        fields = ['sender', 'cac', 'concept', 'amount']

    # Esta linea asegura que al crear una instancia del formulario TransactionForm el campo sender
    # mostrará solo las cuentas bancarias asociadas con el usuario y que estén activas.

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['sender'].queryset = BankAccount.objects.filter(user=user, status=Status.ACTIVE)
