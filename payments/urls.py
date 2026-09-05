from django.urls import path
from payments.views import PaymentSuccessView, PaymentCancelView, stripe_webhook

app_name = "payments"

urlpatterns = [
    path("success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("cancel/", PaymentCancelView.as_view(), name="payment-cancel"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
