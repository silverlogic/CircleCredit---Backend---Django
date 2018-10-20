from rest_framework import serializers

from credit.models import Investment, Vouch, CreditImpact, Loan, Credit


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit


class CreditFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditImpact


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan


class VouchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vouch


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
