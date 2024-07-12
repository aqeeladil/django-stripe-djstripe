
from django.urls import path
from . import views

urlpatterns = [
    # path('subscribe/', views.subscribe, name='subscribe'),
    path('success/', views.subscription_success, name='success'),
    path('cancel/', views.subscription_cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]


