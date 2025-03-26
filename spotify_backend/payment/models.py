from django.db import models

from accounts.models import CustomUser

class SubscriptionPlan(models.Model):
    """Subscription Plans Model"""
    PLAN_TYPES = [
        ('FREE', 'Free'),
        ('INDIVIDUAL', 'Individual Premium'),
        ('FAMILY', 'Family Premium')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_type = models.CharField(
        max_length=20, 
        choices=PLAN_TYPES, 
        default='FREE'
    )
    max_users = models.IntegerField(default=1)
    features = models.JSONField(default=list)

class Subscription(models.Model):
    """User Subscription Model"""
    SUBSCRIPTION_STATUS = [
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired')
    ]

    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=SUBSCRIPTION_STATUS, 
        default='ACTIVE'
    )
    auto_renew = models.BooleanField(default=True)

class Payment(models.Model):
    """ Payment Transactions Model """
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    amout = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50)

