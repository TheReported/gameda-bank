from django import forms

from bank_account.models import BankAccount

from .models import Card


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ['alias', 'bank_account']

    def __init__(self, user, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.active.filter(user=user)


class CardEditForm(CardForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
