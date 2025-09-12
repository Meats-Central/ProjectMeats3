"""
Serializers for licensing models.
"""
from rest_framework import serializers
from .models import SubscriptionPlan, Subscription, Invoice


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionPlan model."""
    
    yearly_discount = serializers.ReadOnlyField()
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'tier', 'monthly_price', 'yearly_price', 'yearly_discount',
            'max_users', 'max_suppliers', 'max_customers', 'max_orders_per_month',
            'has_ai_assistant', 'has_advanced_reporting', 'has_document_processing',
            'has_api_access', 'has_priority_support', 'has_custom_branding',
            'description', 'features', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model."""
    
    plan = SubscriptionPlanSerializer(read_only=True)
    is_active = serializers.ReadOnlyField()
    is_trial = serializers.ReadOnlyField()
    trial_days_remaining = serializers.ReadOnlyField()
    days_until_renewal = serializers.ReadOnlyField()
    usage_limits = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'tenant', 'plan', 'status', 'billing_cycle_anchor',
            'current_period_start', 'current_period_end', 'trial_start', 'trial_end',
            'canceled_at', 'cancel_at_period_end', 'current_users', 'current_suppliers',
            'current_customers', 'current_month_orders', 'is_active', 'is_trial',
            'trial_days_remaining', 'days_until_renewal', 'usage_limits',
            'created_on', 'modified_on'
        ]
        read_only_fields = [
            'id', 'tenant', 'billing_cycle_anchor', 'current_period_start',
            'current_period_end', 'trial_start', 'trial_end', 'canceled_at',
            'created_on', 'modified_on'
        ]

    def get_usage_limits(self, obj):
        """Get usage limits for the subscription."""
        return obj.check_usage_limits()


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model."""
    
    subscription = serializers.StringRelatedField(read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'subscription', 'invoice_number', 'amount_due', 'amount_paid',
            'invoice_date', 'due_date', 'paid_date', 'status', 'period_start',
            'period_end', 'is_overdue', 'created_on'
        ]
        read_only_fields = ['id', 'created_on']


class SubscriptionCreateSerializer(serializers.Serializer):
    """Serializer for creating a new subscription."""
    
    plan_id = serializers.IntegerField()
    billing_cycle = serializers.ChoiceField(
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='monthly'
    )
    trial_days = serializers.IntegerField(default=14, min_value=0, max_value=365)

    def validate_plan_id(self, value):
        """Validate that the plan exists and is active."""
        try:
            plan = SubscriptionPlan.objects.get(id=value, is_active=True)
            return value
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive subscription plan.")


class FeatureCheckSerializer(serializers.Serializer):
    """Serializer for checking feature access."""
    
    feature_name = serializers.CharField()
    has_access = serializers.BooleanField(read_only=True)
    reason = serializers.CharField(read_only=True, required=False)