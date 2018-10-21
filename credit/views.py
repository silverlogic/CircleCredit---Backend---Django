from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from credit.models import Credit, CreditImpact
from credit.serializers import CreditSerializer, CreditImpactSerializer, VouchSerializer, InvestmentSerializer, \
    LoanSerializer


class CreditViewSet(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = CreditSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request):
        user = self.request.user
        credit = Credit.objects.get(user=user)
        serializer = CreditSerializer(credit)
        return Response(serializer.data)


class CreditImpactViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = CreditImpactSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CreditImpact.objects.all()

    def list(self, request):
        user = self.request.user
        credit_impacts = CreditImpact.objects.filter(credit=user.credit)
        serializer = CreditImpactSerializer(credit_impacts, many=True)
        return Response(serializer.data)


class LoanViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = LoanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.credit.loans.all()


class VouchViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = VouchSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.credit.credit_impacts.vouches.all()


class InvestmentViewSet(mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.credit.investments.all()
