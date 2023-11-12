from django import forms

from .models import Card


class CardForm(forms.ModelForm):
    bank_account = forms.CharField(max_length=7)

    class Meta:
        model = Card
        fields = ['alias']


class CardEditForm(forms.ModelForm):
    bank_account = forms.CharField(max_length=7)

    class Meta:
        model = Card
        fields = ['alias']
