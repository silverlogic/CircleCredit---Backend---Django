from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from credit.models import Investment, Vouch, CreditImpact, Loan, Credit


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ('amount',)


class CreditImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditImpact
        fields = ('impact', 'source',)


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('original_amount', 'paid_amount', 'interest', 'description', 'id',)


class PublicLoanSerializer(serializers.ModelSerializer):
    borrower = serializers.SerializerMethodField()
    amount = MoneyField(max_digits=19, decimal_places=2, source='original_amount')

    def get_borrower(self, obj):
        """
        Get user details for public viewers of a loan
        """
        borrower = obj.credit.user
        return {'firstname': borrower.first_name, 'lastname': borrower.last_name}

    class Meta:
        model = Loan
        fields = ('amount', 'borrower', 'description', 'id')


class VouchSerializer(serializers.ModelSerializer):
    loan = serializers.SerializerMethodField

    class Meta:
        model = Vouch
        fields = ('amount', 'loan',)


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ('original_amount', 'paid_amount', 'interest',)
