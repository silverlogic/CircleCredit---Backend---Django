from datetime import timedelta
from django.utils import timezone
from django.db import models
from djmoney.models.fields import MoneyField


class Credit(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="credit")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')

    class Meta:
        verbose_name_plural = 'credit'

    def __str__(self):
        return f'Credit for {self.user.first_name} {self.user.last_name}'


CREDIT_IMPACT_SOURCE = (
    ('LOAN', 'loan'), ('VOUCH', 'vouch'), ('EDUCATION', 'education'), ('INVESTMENT', 'investment'),
    ('BALANCE', 'balance'))


class CreditImpact(models.Model):
    credit = models.ForeignKey('credit.Credit', on_delete=models.CASCADE, related_name="credit_impacts")
    impact = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    source = models.CharField(choices=CREDIT_IMPACT_SOURCE, max_length=12, blank=True)

    def __str__(self):
        return f'Credit impact on {self.credit.user.first_name} {self.credit.user.last_name}\'s Credit'


LOAN_STATUS = (('PENDING', 'pending'), ('ACTIVE', 'active',), ('PAID', 'paid'), ('CANCELLED', 'cancelled'))


def thirty_day_deadline():
    return timezone.now() + timedelta(days=30)


class Loan(models.Model):
    status = models.CharField(choices=LOAN_STATUS, max_length=12, default='PENDING')
    credit = models.ForeignKey('credit.Credit', on_delete=models.CASCADE, related_name='loans', null=True)
    original_amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    interest = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', default='0.00')
    paid_amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', default='0.00')
    description = models.CharField(max_length=256, blank=True)
    due_date = models.DateTimeField(null=True, default=thirty_day_deadline)

    def __str__(self):
        return f'Loan for {self.credit.user.first_name} {self.credit.user.last_name}'


class Payment(models.Model):
    loan = models.ForeignKey('credit.Loan', on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    payment_date = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'Payment for Loan {self.loan.pk}'


VOUCH_STATUS = (('INVITED', 'invited',), ('ACCEPTED', 'accepted'), ('DECLINED', 'declined'))


class Vouch(models.Model):
    status = models.CharField(choices=VOUCH_STATUS, max_length=12, default="INVITED")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', blank=True, default='0.00')
    loan = models.ForeignKey('credit.Loan', on_delete=models.SET_NULL, null=True, related_name='vouches')
    vouching_user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    credit_impact = models.OneToOneField('credit.CreditImpact', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'vouches'

    def __str__(self):
        return 'Vouch'


class Investment(models.Model):
    status = models.CharField(choices=LOAN_STATUS, max_length=12, default='PENDING')
    credit = models.ForeignKey('credit.Credit', on_delete=models.CASCADE, related_name='investments', null=True)
    original_amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    interest = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', default='0.00')
    paid_amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', default='0.00')
    description = models.CharField(max_length=256, blank=True)
    due_date = models.DateTimeField(null=True, default=timezone.now() + timedelta(days=30))
    loan = models.ForeignKey('credit.Loan', on_delete=models.SET_NULL, null=True, related_name='investments2')
    credit_impact = models.OneToOneField('credit.CreditImpact', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Investment {self.id}'
