from rest_framework import serializers

from credit.models import Investment, Vouch, CreditImpact, Loan, Credit


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ('amount',)


class CreditImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditImpact
        fields = ('impact', 'source')


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('original_amount', 'paid_amount', 'interest',)


class VouchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vouch


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ('original_amount', 'paid_amount', 'interest',)
