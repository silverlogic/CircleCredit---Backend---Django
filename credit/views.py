from django.core.exceptions import ObjectDoesNotExist
from fcm_django.models import FCMDevice
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from credit.calculations import calculate_interest
from credit.models import Credit, CreditImpact, Loan, Vouch, Investment
from credit.serializers import CreditSerializer, CreditImpactSerializer, VouchSerializer, InvestmentSerializer, \
    LoanSerializer, PublicLoanSerializer, LoanVouchSerializer
from users.models import User


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
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = LoanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.credit.loans.all()

    def list(self, request):
        user = self.request.user
        loans = Loan.objects.filter(credit__user=user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = self.request.user
        request.data['credit'] = user.credit.id
        request.data['interest'] = calculate_interest(user.credit, request.data['original_amount'])
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            credit_impact_serializer = CreditImpactSerializer(data=
                                                              {'source': 'LOAN', 'credit': user.credit.id,
                                                               'impact': '-' + str(request.data['original_amount'])})
            if credit_impact_serializer.is_valid():
                credit_impact_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({**serializer.errors, **credit_impact_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=True, methods=['get'])
    def vouches(self, request, pk):
        user = self.request.user
        try:
            loan = Loan.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user == loan.credit.user:
            serializer = LoanVouchSerializer(loan.vouches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class VouchViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = VouchSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Vouch.objects.all()

    def list(self, request):
        user = self.request.user
        vouches = Vouch.objects.filter(vouching_user=user)
        serializer = VouchSerializer(vouches, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = self.request.user
        serializer = VouchSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            try:
                device = FCMDevice.objects.get(user=instance.vouching_user)
                device.send_message(data={'id': instance.id})
            except ObjectDoesNotExist:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        user = self.request.user
        try:
            vouch = Vouch.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if vouch.vouching_user.id != user.id:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        vouching_status = request.data['status']
        if vouching_status == 'ACCEPTED':
            serializer = CreditImpactSerializer(data=
                                                {'source': 'VOUCH', 'credit': user.credit.id,
                                                 'impact': '-' + str(request.data['amount'])})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        vouch.status = vouching_status
        vouch.save()
        vouch_serializer = VouchSerializer(vouch)
        return Response(vouch_serializer.data, status=status.HTTP_200_OK)


class InvestmentViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = (IsAuthenticated,)
    investment = Investment.objects.all()

    def create(self, request):
        user = self.request.user
        request.data['credit'] = user.credit
        serializer = InvestmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user = self.request.user
        investments = Investment.objects.filter(credit__user=user)
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
