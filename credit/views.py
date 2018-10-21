import braintree
import json

import requests as requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from fcm_django.models import FCMDevice
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from credit.calculations import calculate_interest
from credit.models import Credit, CreditImpact, Loan, Vouch, Investment
from credit.serializers import CreditSerializer, CreditImpactSerializer, VouchSerializer, InvestmentSerializer, \
    LoanSerializer, PublicLoanSerializer, LoanVouchSerializer
from users.models import User
from users.serializers import UserSerializer


class CreditViewSet(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = CreditSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request):
        user = self.request.user
        credit = Credit.objects.get(user=user)
        serializer = CreditSerializer(credit)
        return Response(serializer.data)


def synchrony_credit_score(request):
    response = requests.get('https://api-stg.syf.com/m2020/credit/customers/1/profile',
                             headers={'Authorization': f'Bearer {settings.SYNCHRONY_ACCESS_TOKEN}'})
    return JsonResponse(response.json())


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

    def partial_update(self, request, pk):
        loan_status = request.data['status']
        try:
            loan = Loan.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Could not find loan to update.'}, status=status.HTTP_400_BAD_REQUEST)
        if loan_status == 'ACTIVE':
            # Go through loan and make investments active, and post payment
            if loan.investments.all() is not None:
                for investment in loan.investments.all():
                    if investment.status != 'ACTIVE':
                        investment.status = 'ACTIVE'
                        gateway = braintree.BraintreeGateway(
                            braintree.Configuration(
                                braintree.Environment.Sandbox,
                                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                public_key=settings.BRAINTREE_PUBLIC_KEY,
                                private_key=settings.BRAINTREE_PRIVATE_KEY
                            )
                        )
                        response = gateway.transaction.sale({
                            'amount': str(investment.original_amount).replace('$', ''),
                            'payment_method_nonce': investment.credit.user.paypal_token,
                            'options': {
                                'submit_for_settlement': True
                            }
                        })
                        if response.is_success is not True:
                            return Response({'error': 'Failed to payout investments.'},
                                            status=status.HTTP_400_BAD_REQUEST)
                        investment.save()
            # Now, use PayPal Payouts to transfer loan from CreditCircle to borrower
            data = {
                'sender_batch_header': {'sender_batch_id': '2014021801', 'email_subject': 'CreditCircle Loan Payment',
                                        'email_message': 'Your CreditCircle loan has been credited to your PayPal account.'},
                'items': [{'recipient_type': 'EMAIL',
                           'amount': {'value': str(loan.original_amount).replace('$', '').replace(',', ''),
                                      'currency': 'USD'},
                           'note': 'Thanks for using CreditCircle!', 'sender_item_id': '2014021801',
                           'receiver': loan.credit.user.email}]
            }
            print(str(loan.original_amount).replace('$', ''))
            json_data = json.dumps(data)
            response = requests.post('https://api.sandbox.paypal.com/v1/payments/payouts',
                                     headers={'Content-Type': 'application/json',
                                              'Authorization': f'Bearer {settings.PAYPAL_ACCESS_TOKEN}'},
                                     data=json_data)
            if not response.ok:
                return Response({'error': 'Failed to payout loan.'}, status=status.HTTP_400_BAD_REQUEST)
            loan.status = loan_status
            loan.save()
        loan_serializer = LoanSerializer(loan)
        return Response(loan_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def calculate_interest(self, request):
        user = self.request.user
        return Response({'interest': calculate_interest(user.credit, request.data['original_amount'])})

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

    def retrieve(self, request, pk):
        user = self.request.user
        try:
            vouch = Vouch.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response('Not Found', status=status.HTTP_404_NOT_FOUND)
        if vouch.loan.credit.user != user or vouch.vouching_user != user:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = VouchSerializer(vouch)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
                device.send_message(
                    data={'id': instance.id, 'name': user.first_name + ' ' + user.last_name, 'type': 'requested'})
            except ObjectDoesNotExist:
                return Response({'error': 'Could not find device for push notification.'},
                                status=status.HTTP_400_BAD_REQUEST)
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
        # Assign credit impact
        if vouching_status == 'ACCEPTED':
            serializer = CreditImpactSerializer(data=
                                                {'source': 'VOUCH', 'credit': user.credit.id,
                                                 'impact': '-' + str(request.data['amount'])})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        vouch.status = vouching_status
        vouch.amount = request.data['amount']
        vouch.save()
        # Get amounts vouched and invested
        investment_amount = request.data['investment']
        vouch_amount = request.data['amount']
        request.data.pop('investment')
        # Create a pending investment from the amount
        investment_serializer = InvestmentSerializer(data=
                                                     {'original_amount': investment_amount, 'interest': 5,
                                                      'loan': vouch.loan.id, 'credit': user.credit.id})
        if investment_serializer.is_valid():
            investment_serializer.save()
        else:
            return Response(investment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Serialize vouch, create push notification, and return response
        vouch_serializer = VouchSerializer(vouch)
        try:
            borrower = vouch.loan.credit.user.id
            device = FCMDevice.objects.get(user=borrower)
            user_serializer = UserSerializer(vouch.vouching_user)
            device.send_message(
                data={'vouching_user': user_serializer.data, 'vouch_amount': vouch_amount,
                      'investment_amount': investment_amount, 'type': 'accepted'})
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
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
        request.data['credit'] = user.credit.id
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

    def retrieve(self, request, pk):
        user = self.request.user
        investments = Investment.objects.filter(credit__user=user)
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
