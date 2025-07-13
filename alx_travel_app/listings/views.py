from django.shortcuts import render
import requests
import uuid
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment

class InitiatePaymentView(APIView):
    def post(self, request):
        amount = request.data.get("amount")
        email = request.data.get("email")
        booking_reference = request.data.get("booking_reference")

        if not all([amount, email, booking_reference]):
            return Response({"error": "Missing required fields"}, status=400)

        tx_ref = str(uuid.uuid4())
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }
        data = {
            "amount": amount,
            "currency": "ETB",
            "email": email,
            "tx_ref": tx_ref,
            "callback_url": f"http://localhost:8000/api/payments/verify/{tx_ref}/",
            "return_url": "http://localhost:8000/payment-success/",
            "customization": {
                "title": "Travel Booking",
                "description": "Payment for travel booking",
            }
        }

        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=data, headers=headers)

        if response.status_code == 200:
            Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                transaction_id=tx_ref,
                status="Pending"
            )
            return Response(response.json(), status=200)
        return Response({"error": "Failed to initiate payment"}, status=500)


class VerifyPaymentView(APIView):
    def get(self, request, tx_ref):
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }

        response = requests.get(f"https://api.chapa.co/v1/transaction/verify/{tx_ref}", headers=headers)
        if response.status_code == 200:
            data = response.json().get("data", {})
            status_code = data.get("status")

            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                if status_code == "success":
                    payment.status = "Completed"
                else:
                    payment.status = "Failed"
                payment.save()
            except Payment.DoesNotExist:
                return Response({"error": "Transaction not found"}, status=404)

            return Response(data, status=200)

        return Response({"error": "Verification failed"}, status=500)


