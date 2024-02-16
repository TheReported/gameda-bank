from django import forms

from card.models import Card

from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['business', 'pin', 'amount', 'ccc']

    def __init__(self, user, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['ccc'].queryset = Card.active.filter(bank_account__user=user)
