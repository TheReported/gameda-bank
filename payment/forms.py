from django import forms
from django.contrib.auth.hashers import check_password

from card.models import Card

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['business', 'ccc', 'pin', 'amount']

    def clean_ccc(self):
        cd = self.cleaned_data
        card = Card.objects.get(code=cd['ccc'])
        if card:
            return cd['ccc']
        raise forms.ValidationError('Client card code does not exists')

    def clean_pin(self):
        cd = self.cleaned_data
        card = Card.objects.get(code=cd['ccc'])
        if check_password(cd['pin'], card.pin):
            return cd['pin']
        raise forms.ValidationError('Pin code does not match')
