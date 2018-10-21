import json
import uuid
import base64
import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        user = self.request.user
        friends = user.friends
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def verify_document(self, request, pk):
        document_front = request.data["document_front"]
        document_back = request.data["document_back"]
        transactionId = uuid.uuid1()
        response = requests.post('https://sandbox.api.visa.com/identitydocuments/v1/documentauthentication',
                                 cert=(settings.VISA_CLIENT_CERT, settings.VISA_PRIVATE_KEY),
                                 auth=(settings.VISA_USER_ID, settings.VISA_USER_PASSWORD),
                                 data={"documentFront": document_front, "document_back": document_back,
                                       "jsonMessage": {"messageTraceId": transactionId}})
        return Response(response.json())

    @action(detail=True, methods=['post'])
    def verify_data(self, request, pk):
        data = """
        {
            "userDataRequest": {
            "messageTraceId": "ac198ded-e204-4ad9-aae7-bfc55f3a0043",
            "name": {
            "first": "Rosetta",
            "last": "Jones"
            },
            "address": {
            "street": "1000 Main St",
            "city": "San Francisco",
            "region": "CA",
            "country": "US",
            "postcode": "94107"
            },
            "phone": {
            "countryCode": "1",
            "number": "4155551234"
            },
            "email": {
            "display": "Rosetta Jones",
            "address": "abcxyz@example.com"
            },
            "ipAddress": "23.200.140.110"
            }
        }
        """
        response = requests.post('https://sandbox.api.visa.com/userdata/v1/attributes',
                                 cert=(settings.VISA_CLIENT_CERT, settings.VISA_PRIVATE_KEY),
                                 auth=(settings.VISA_USER_ID, settings.VISA_USER_PASSWORD),
                                 headers={"Authorization": base64.b64encode(
                                     json.dumps({settings.VISA_USER_ID: settings.VISA_USER_PASSWORD}).encode())},
                                 data=data)
        return Response(response.json())

    @action(detail=True, methods=['post'])
    def get_transactions(self, request, pk):
        user = self.request.user
        # You would use a user's PayPal token here to make the API call and retrieve their data.
        response = requests.post('https://api.sandbox.paypal.com/v1/activities/activities',
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {settings.PAYPAL_ACCESS_TOKEN}'}, )
        if not response.ok:
            return Response({'error': 'Failed to fetch transactions'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.json(), status=status.HTTP_200_OK)
