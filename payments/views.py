from django.shortcuts import render
from payments.models import Payment
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


class PaymentSuccessView(APIView):
    def get(self, request):
        return Response(
            {
                "detail": "Thank you! Your payment is being processed. It may take a few minutes to update the status."
            }
        )


class PaymentCancelView(APIView):
    def get(self, request):
        return Response(
            {"detail": "Payment was cancelled. You can try again later."},
            status=status.HTTP_200_OK,
        )


@csrf_exempt  # Turn off CSRF, since we receive a response from the Stripe server
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None

    try:
        # Проверяем, что запрос реально пришел от Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Неверный payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Неверная подпись
        return HttpResponse(status=400)

    # Если оплата прошла успешно
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id")

        try:
            payment = Payment.objects.get(session_id=session_id)
            payment.status = Payment.StatusChoices.PAID
            payment.save()
            # Опционально: тут можно вызвать Celery-таску, чтобы отправить в Telegram "Оплата успешно получена!"
        except Payment.DoesNotExist:
            pass

    # Всегда возвращаем 200, чтобы Stripe понял, что мы получили сообщение
    return HttpResponse(status=200)
