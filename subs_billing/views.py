
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .stripe_utils import create_stripe_customer, create_stripe_subscription
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
import djstripe.models
# from . import models
from .models import Subscription
import logging
import os
from django.http import JsonResponse, HttpResponse


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

'''
@login_required
def subscribe(request):
    if request.method == 'POST':
        # plan_id = request.POST['plan_id']
        plan_id = request.POST.get['plan_id']
        user = request.user
        customer = create_stripe_customer(user.email)
        subscription = create_stripe_subscription(customer.id, plan_id)
        # Save subscription details in your database if needed
        return redirect('subscription_success')
    return render(request, 'billing/subscribe.html', {'settings': settings})
'''

@login_required
def subscription_success(request):
    return render(request, 'billing/subscription_success.html')

@login_required
def subscription_cancel(request):
    # user = request.user
    # Retrieve and cancel the user's subscription
    # For example, use stripe.Subscription.delete(subscription_id)
    # subscription = None  # Replace with actual subscription retrieval and cancellation logic
    return render(request, 'billing/subscription_cancel.html')
    # return render(request, 'billing/subscription_cancel.html', {'subscription': subscription})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            # payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            payload, sig_header, os.environ['DJSTRIPE_SECRET_KEY']
        )
    except ValueError as e:
        logger.error("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature")
        return HttpResponse(status=400)

    # Process the webhook event
    try:
        djstripe_event = djstripe.models.Event.process(data=event)
    except Exception as e:
        logger.error("Failed to process webhook", exc_info=True)
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        # Handle subscription creation event
        handle_subscription_created(subscription)
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_payment_succeeded(invoice)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Handle subscription deletion event
        handle_subscription_deleted(subscription)

    # Add more event handlers as needed

    return HttpResponse(status=200)

def handle_payment_succeeded(invoice):
    # Implement your logic to handle successful payment
    pass

def handle_subscription_created(subscription):
    # Implement your logic to handle subscription creation
    pass

def handle_subscription_deleted(subscription):
    # Implement your logic to handle subscription cancellation
    pass
# billing/views.py

@login_required
def subscription_details(request):
    user = request.user
    # Retrieve subscription details from your database or Stripe
    # For example, use stripe.Subscription.retrieve(subscription_id)
    subscription = None  # Replace with actual subscription retrieval logic
    return render(request, 'billing/subscription_details.html', {'subscription': subscription})




@login_required
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        price_id = request.POST.get('price_id', None)

        if not price_id:
            # return redirect('home')
            return JsonResponse({"error": "price_lookup_key not found"}, status=400)
        
        try:
            YOUR_DOMAIN = "http://localhost:8000"
            checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=request.build_absolute_uri('/billing/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/billing/cancel/'),
            # success_url=DOMAIN + 'success?session_id={CHECKOUT_SESSION_ID}',
            # cancel_url=DOMAIN + 'cancel/',
            # customer_email=request.user.email,
            )

            return redirect(checkout_session.url, code=303)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            # return JsonResponse({"error": str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
     

        
'''
def create_checkout_session(request) -> HttpResponse:
    price_lookup_key = request.POST['price_lookup_key']
    try:
        prices = stripe.Price.list(lookup_keys=[price_lookup_key], expand=['data.product'])
        price_item = prices.data[0]

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {'price': price_item.id, 'quantity': 1},
                # You could add differently priced services here, e.g., standard, business, first-class.
            ],
            mode='subscription',
            success_url=DOMAIN + reverse('success') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=DOMAIN + reverse('cancel')
        )

            # We connect the checkout session to the user who initiated the checkout.
            models.CheckoutSessionRecord.objects.create(
            user=request.user,
            stripe_checkout_session_id=checkout_session.id,
            stripe_price_id=price_item.id,
        )

        return redirect(
            checkout_session.url,  # Either the success or cancel url.
            code=303
        )
    except Exception as e:
        print(e)
        return HttpResponse("Server error", status=500)
'''