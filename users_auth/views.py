from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import random
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import SMSSerializer, VerifySMSSerializer
from django.conf import settings

User = get_user_model()
SMS_KEY = settings.SMS_KEY


class SMSLoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def send_sms(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = str(random.randint(100000, 999999))
            url = 'https://2yd5jm.api.infobip.com/sms/2/text/advanced'

            headers = {
                'Authorization': f'App {SMS_KEY}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            payload = {
                'messages': [{
                    'from': 'Sardor',
                    'destinations': [{'to': phone_number}],
                    'text': f'Sizning tasdiqlash kodingiz: {verification_code}'
                }]
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                print(f"Infobip Status: {response.status_code}")
                print(f"Infobip Response: {response.text}")

                if response.status_code == 200:
                    cache.set(phone_number, verification_code, 300)
                    print(f"TERMINALDA KODNI KO'RISH: {verification_code}")
                    return Response({"message": "SMS yuborildi"}, status=status.HTTP_200_OK)

                return Response({"message": "Infobip xatosi", "detail": response.json()}, status=400)
            except Exception as e:
                return Response({"message": f"Server xatosi: {str(e)}"}, status=500)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_sms(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']

            cached_code = cache.get(phone_number)
            print(f"Phone: {phone_number}, Sent Code: {verification_code}, Cached: {cached_code}")

            if cached_code and verification_code == cached_code:
                user, created = User.objects.get_or_create(phone_number=phone_number)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

            return Response({"message": "Kod xato yoki muddati o'tgan"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
