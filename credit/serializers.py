from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from credit.models import Investment, Vouch, CreditImpact, Loan, Credit, Payment
from users.serializers import UserSerializer


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ('amount',)
        read_only_fields = ('amount',)


class CreditImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditImpact
        fields = ('impact', 'source', 'credit',)
        extra_kwargs = {'credit': {'write_only': True}}


class LoanSerializer(serializers.ModelSerializer):
    credit = serializers.PrimaryKeyRelatedField(queryset=Credit.objects.all())

    class Meta:
        model = Loan
        fields = ('original_amount', 'paid_amount', 'interest', 'status', 'description', 'credit', 'id', 'due_date')
        read_only_fields = ('paid_amount', 'id', 'due_date')
        extra_kwargs = {'credit': {'write_only': True}}


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
        fields = ('amount', 'borrower', 'description', 'id',)


class VouchSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(VouchSerializer, self).to_representation(instance)
        data['loan'] = PublicLoanSerializer(instance.loan).data
        return data

    class Meta:
        model = Vouch
        fields = ('amount', 'loan', 'vouching_user', 'status', 'id',)
        read_only_fields = ('id',)


class LoanVouchSerializer(serializers.ModelSerializer):
    vouching_user = UserSerializer()

    class Meta:
        model = Vouch
        fields = ('amount', 'loan', 'vouching_user', 'status')


class InvestmentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(InvestmentSerializer, self).to_representation(instance)
        data['loan'] = PublicLoanSerializer(instance.loan).data
        return data

    class Meta:
        model = Investment
        fields = ('original_amount', 'paid_amount', 'interest', 'loan', 'status', 'id', 'credit')
        read_only_fields = ('paid_amount', 'id',)
        extra_kwargs = {'credit': {'write_only': True}}


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('loan', 'amount', 'payment_date', 'due_date')
