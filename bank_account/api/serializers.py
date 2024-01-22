from rest_framework import serializers

from bank_account.models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['alias', 'balance', 'status', 'code']
