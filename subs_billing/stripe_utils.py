
import stripe
import os
from django.conf import settings

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

def create_stripe_customer(email):
    return stripe.Customer.create(email=email)

def create_stripe_subscription(customer_id, plan_id):
    return stripe.Subscription.create(
        customer=customer_id,
        items=[{'plan': plan_id}]
    )

def get_stripe_subscription(subscription_id):
    return stripe.Subscription.retrieve(subscription_id)
