from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from credit.models import Credit, CreditImpact, Loan
from credit.serializers import CreditSerializer, CreditImpactSerializer, VouchSerializer, InvestmentSerializer, \
    LoanSerializer, PublicLoanSerializer


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


class LoanViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = LoanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.credit.loans.all()

    def retrieve(self, request, pk):
        user = self.request.user
        try:
            loan = Loan.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if loan.credit.user != user:
            serializer = PublicLoanSerializer(loan)
        else:
            serializer = LoanSerializer(loan)
        return Response(serializer.data)


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
