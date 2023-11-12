from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    ccc = forms.CharField(max_length=7)

    class Meta:
        model = Payment
        fields = ['business', 'pin', 'amount']
