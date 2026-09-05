import stripe
from django.conf import settings
from rest_framework.reverse import reverse

# Initialize Stripe by secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(payment, request):
    """
    Create payment session in Stripe and return URL for user redirecting.
    """
    # Calculate sum for pay in cents
    unit_amount = int(payment.money_to_pay * 100)

    success_url = (
        request.build_absolute_uri(reverse("payments:payment-success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = request.build_absolute_uri(reverse("payments:payment-cancel"))

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Library Borrowing #{payment.borrowing.id}",
                            "description": f"Book rental payment for {payment.borrowing.book.title}",
                        },
                        "unit_amount": unit_amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )

        payment.session_id = session.id
        payment.session_url = session.url
        payment.save()

        return session.url
    except Exception as e:
        raise ValueError(f"Stripe error: {str(e)}")
