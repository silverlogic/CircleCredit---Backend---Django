from django.contrib import admin

from credit.models import Credit, CreditImpact, Loan, Vouch, Investment


class CreditAdmin(admin.ModelAdmin):
    pass


class CreditImpactAdmin(admin.ModelAdmin):
    pass


class LoanAdmin(admin.ModelAdmin):
    pass


class VouchAdmin(admin.ModelAdmin):
    pass


class InvestmentAdmin(admin.ModelAdmin):
    pass


admin.site.register((Credit,
                     CreditImpact,
                     Loan,
                     Vouch,
                     Investment,))
