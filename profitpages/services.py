from random import random

import stripe

from config.settings import DEBUG, STRIPE_API_KEY


def send_sms(phone):
    random_code = random.randint(100000, 999999)
    return random_code


stripe.api_key = STRIPE_API_KEY

def new_create_stripe_session(price):
    if DEBUG:
        url = "127.0.0.1:8000"
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "rub",
                    "unit_amount": price * 100,
                    "product_data": {
                        "name": "Подписка сервиса ProfitPages",
                    },
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=f"http://{url}/payment_success",
        cancel_url=f"http://{url}/payment_cancel",

    )
    return session.get("id"), session.get("url")
