from django import forms

from .models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['alias', 'bank_account', 'status']
