from django.urls import path
from rest_framework import routers

from credit.views import CreditViewSet, CreditImpactViewSet, LoanViewSet, InvestmentViewSet, VouchViewSet

router = routers.SimpleRouter()
router.register(r'loans', LoanViewSet, 'loan')
router.register(r'investments', InvestmentViewSet, 'investment')
router.register(r'vouches', VouchViewSet, 'vouches')
urlpatterns = router.urls

urlpatterns += [
    path('credit/', CreditViewSet.as_view({'get': 'retrieve'})),
    path('credit-factors/', CreditImpactViewSet.as_view({'get': 'list'})),
]
