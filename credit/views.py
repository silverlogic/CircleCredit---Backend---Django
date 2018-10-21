from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from credit.calculations import calculate_interest
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

    def create(self, request):
        user = self.request.user
        request.data['credit'] = user.credit.id
        request.data['interest'] = calculate_interest(user.credit, request.data['original_amount'])
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def calculate_interest(self, request):
        user = self.request.user
        return Response({"interest": calculate_interest(user.credit, request.data['original_amount'])})


class VouchViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = VouchSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.credit.credit_impacts.vouches.all()

    def create(self, request):
        # SEND PUSH TO FIREBASE
        serializer = VouchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        pass
        # If accepted, add credit factors
        # If declined, delete object

class InvestmentViewSet(mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.credit.investments.all()
