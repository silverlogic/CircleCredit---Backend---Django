from rest_framework import viewsets

from credit.serializers import CreditSerializer, CreditFactorSerializer, VouchSerializer, InvestmentSerializer, \
    LoanSerializer


class CreditViewSet(viewsets.ModelViewSet):
    serializer = CreditSerializer

    def list(self):



class CreditFactorViewSet(viewsets.ModelViewSet):
    serializer = CreditFactorSerializer


class LoanViewSet(viewsets.ModelViewSet):
    serializer = LoanSerializer


class VouchViewSet(viewsets.ModelViewSet):
    serializer = VouchSerializer


class InvestmentViewSet(viewsets.ModelViewSet):
    serializer = InvestmentSerializer
