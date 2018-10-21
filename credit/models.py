from django.db import models
from djmoney.models.fields import MoneyField


class Credit(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="credit")
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')

    class Meta:
        verbose_name_plural = 'credit'

    def __str__(self):
        return f'Credit for {self.user.first_name} {self.user.last_name}'


class CreditImpact(models.Model):
    credit = models.ForeignKey('credit.Credit', on_delete=models.CASCADE, related_name="credit_impacts")
    impact = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')

    def __str__(self):
        return f'Credit impact on {self.credit.user.first_name} {self.credit.user.last_name}\'s Credit'


class Loan(models.Model):
    credit = models.ForeignKey('credit.Credit', on_delete=models.CASCADE, related_name='loans')
    original_amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    interest = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', default='0.00')
    paid_amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD', default='0.00')

    def __str__(self):
        return f'Loan for {self.credit.user.first_name} {self.credit.user.last_name}'


class Vouch(models.Model):
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    loan = models.ForeignKey('credit.Loan', on_delete=models.SET_NULL, null=True, related_name='vouches')
    credit_impact = models.OneToOneField('credit.CreditImpact', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'vouches'

    def __str__(self):
        return f'Vouch from {self.credit_impact.credit.user.first_name} {self.credit_impact.credit.user.last_name} to' \
               f'to {self.loan.credit.user.first_name} {self.loan.credit.user.last_name}'


class Investment(Loan):
    """ Inherits credit (lender's), original_amount, interest, paid_amount"""
    loan = models.ForeignKey('credit.Loan', on_delete=models.SET_NULL, null=True, related_name='investments')
    credit_impact = models.OneToOneField('credit.CreditImpact', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Investment from {self.credit.user.first_name} {self.credit.user.last_name} to' \
               f'to {self.loan.credit.user.first_name} {self.loan.credit.user.last_name}'
