"""
Licensing models for ProjectMeats.

Manages subscription plans, billing, and feature access control
for the multi-tenant SaaS platform.
"""
import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta

from apps.core.models import Tenant, TimestampModel


class PlanTier(models.TextChoices):
    """Subscription plan tiers."""
    FREE = "free", "Free"
    BASIC = "basic", "Basic"
    PROFESSIONAL = "professional", "Professional"
    ENTERPRISE = "enterprise", "Enterprise"


class SubscriptionStatus(models.TextChoices):
    """Subscription status choices."""
    ACTIVE = "active", "Active"
    PAST_DUE = "past_due", "Past Due"
    CANCELED = "canceled", "Canceled"
    INCOMPLETE = "incomplete", "Incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired", "Incomplete Expired"
    TRIALING = "trialing", "Trialing"
    UNPAID = "unpaid", "Unpaid"


class SubscriptionPlan(models.Model):
    """Subscription plan configuration."""
    
    name = models.CharField(max_length=100, unique=True)
    tier = models.CharField(
        max_length=20,
        choices=PlanTier.choices,
        help_text="Plan tier level"
    )
    stripe_price_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Stripe Price ID for this plan"
    )
    
    # Pricing
    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Monthly price in USD"
    )
    yearly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Yearly price in USD (optional)"
    )
    
    # Features and limits
    max_users = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of users (null = unlimited)"
    )
    max_suppliers = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of suppliers (null = unlimited)"
    )
    max_customers = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of customers (null = unlimited)"
    )
    max_orders_per_month = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum orders per month (null = unlimited)"
    )
    
    # Feature flags for this plan
    has_ai_assistant = models.BooleanField(default=True)
    has_advanced_reporting = models.BooleanField(default=True)
    has_document_processing = models.BooleanField(default=True)
    has_api_access = models.BooleanField(default=False)
    has_priority_support = models.BooleanField(default=False)
    has_custom_branding = models.BooleanField(default=False)
    
    # Metadata
    description = models.TextField(blank=True)
    features = models.JSONField(
        default=list,
        help_text="List of feature descriptions for marketing"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscription_plans"
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"
        ordering = ["monthly_price"]

    def __str__(self):
        return f"{self.name} (${self.monthly_price}/month)"

    @property
    def yearly_discount(self):
        """Calculate yearly discount percentage."""
        if not self.yearly_price:
            return 0
        monthly_yearly = self.monthly_price * 12
        if monthly_yearly == 0:
            return 0
        return ((monthly_yearly - self.yearly_price) / monthly_yearly) * 100


class Subscription(TimestampModel):
    """Subscription model for tenant billing."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="subscription"
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        help_text="Current subscription plan"
    )
    
    # Stripe integration
    stripe_subscription_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Stripe subscription ID"
    )
    stripe_customer_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Stripe customer ID"
    )
    
    # Subscription details
    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.TRIALING,
        help_text="Current subscription status"
    )
    
    # Billing cycle
    billing_cycle_anchor = models.DateTimeField(
        help_text="When the billing cycle starts"
    )
    current_period_start = models.DateTimeField(
        help_text="Start of the current billing period"
    )
    current_period_end = models.DateTimeField(
        help_text="End of the current billing period"
    )
    
    # Trial information
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    
    # Cancellation
    canceled_at = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    
    # Usage tracking
    current_users = models.PositiveIntegerField(default=1)
    current_suppliers = models.PositiveIntegerField(default=0)
    current_customers = models.PositiveIntegerField(default=0)
    current_month_orders = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = "subscriptions"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name} ({self.status})"

    @property
    def is_active(self):
        """Check if subscription is currently active."""
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]

    @property
    def is_trial(self):
        """Check if subscription is in trial period."""
        return (
            self.status == SubscriptionStatus.TRIALING
            and self.trial_end
            and timezone.now() < self.trial_end
        )

    @property
    def trial_days_remaining(self):
        """Get remaining trial days."""
        if not self.is_trial:
            return 0
        remaining = self.trial_end - timezone.now()
        return max(0, remaining.days)

    @property
    def days_until_renewal(self):
        """Get days until next billing cycle."""
        if not self.current_period_end:
            return 0
        remaining = self.current_period_end - timezone.now()
        return max(0, remaining.days)

    def can_use_feature(self, feature_name):
        """Check if subscription allows using a specific feature."""
        if not self.is_active:
            return False
            
        # Check plan features
        feature_map = {
            'ai_assistant': self.plan.has_ai_assistant,
            'advanced_reporting': self.plan.has_advanced_reporting,
            'document_processing': self.plan.has_document_processing,
            'api_access': self.plan.has_api_access,
            'priority_support': self.plan.has_priority_support,
            'custom_branding': self.plan.has_custom_branding,
        }
        
        return feature_map.get(feature_name, False)

    def check_usage_limits(self):
        """Check if tenant is within usage limits."""
        limits = {}
        
        if self.plan.max_users and self.current_users > self.plan.max_users:
            limits['users'] = {
                'current': self.current_users,
                'limit': self.plan.max_users,
                'exceeded': True
            }
            
        if self.plan.max_suppliers and self.current_suppliers > self.plan.max_suppliers:
            limits['suppliers'] = {
                'current': self.current_suppliers,
                'limit': self.plan.max_suppliers,
                'exceeded': True
            }
            
        if self.plan.max_customers and self.current_customers > self.plan.max_customers:
            limits['customers'] = {
                'current': self.current_customers,
                'limit': self.plan.max_customers,
                'exceeded': True
            }
            
        if self.plan.max_orders_per_month and self.current_month_orders > self.plan.max_orders_per_month:
            limits['orders'] = {
                'current': self.current_month_orders,
                'limit': self.plan.max_orders_per_month,
                'exceeded': True
            }
        
        return limits

    @classmethod
    def create_free_trial(cls, tenant, trial_days=14):
        """Create a free trial subscription for a tenant."""
        # Get or create free plan
        free_plan, _ = SubscriptionPlan.objects.get_or_create(
            tier=PlanTier.FREE,
            defaults={
                'name': 'Free Trial',
                'monthly_price': Decimal('0.00'),
                'description': 'Free trial with basic features',
                'features': [
                    'Up to 5 suppliers',
                    'Up to 10 customers',
                    'Basic AI assistant',
                    'Standard reporting'
                ],
                'max_suppliers': 5,
                'max_customers': 10,
                'max_orders_per_month': 50,
                'has_ai_assistant': True,
                'has_advanced_reporting': False,
                'has_document_processing': True,
            }
        )
        
        now = timezone.now()
        trial_end = now + timedelta(days=trial_days)
        
        subscription = cls.objects.create(
            tenant=tenant,
            plan=free_plan,
            status=SubscriptionStatus.TRIALING,
            billing_cycle_anchor=now,
            current_period_start=now,
            current_period_end=trial_end,
            trial_start=now,
            trial_end=trial_end
        )
        
        return subscription


class Invoice(TimestampModel):
    """Invoice model for subscription billing."""
    
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="invoices"
    )
    stripe_invoice_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Stripe invoice ID"
    )
    
    # Invoice details
    invoice_number = models.CharField(max_length=50)
    amount_due = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Dates
    invoice_date = models.DateTimeField()
    due_date = models.DateTimeField()
    paid_date = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('void', 'Void'),
            ('uncollectible', 'Uncollectible'),
        ],
        default='draft'
    )
    
    # Billing period
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    class Meta:
        db_table = "subscription_invoices"
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ["-invoice_date"]

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.subscription.tenant.name}"

    @property
    def is_overdue(self):
        """Check if invoice is overdue."""
        return (
            timezone.now() > self.due_date
            and self.status == 'open'
        )
