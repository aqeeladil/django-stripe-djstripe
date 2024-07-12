
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# class CheckoutSessionRecord(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, help_text="The user who initiated the checkout."
#     )
#     stripe_customer_id = models.CharField(max_length=255)
#     stripe_checkout_session_id = models.CharField(max_length=255)
#     stripe_price_id = models.CharField(max_length=255)
#     has_access = models.BooleanField(default=False)
#     is_completed = models.BooleanField(default=False)


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s subscription"