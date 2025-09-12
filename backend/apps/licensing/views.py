"""
API views for licensing and subscription management.
"""
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.core.models import Tenant
from .models import SubscriptionPlan, Subscription, Invoice
from .serializers import (
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    InvoiceSerializer,
    SubscriptionCreateSerializer,
    FeatureCheckSerializer,
)

# Configure Stripe (in production, use environment variable)
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_...')


class SubscriptionPlanListView(generics.ListAPIView):
    """List available subscription plans."""
    
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscriptionDetailView(generics.RetrieveAPIView):
    """Get subscription details for current tenant."""
    
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Get subscription for current user's tenant."""
        # For now, get the first tenant (in production, use middleware to determine tenant)
        tenant = Tenant.objects.filter(owner=self.request.user).first()
        if not tenant:
            tenant = Tenant.objects.first()  # Fallback for development
        
        subscription, created = Subscription.objects.get_or_create(
            tenant=tenant,
            defaults={
                'plan': SubscriptionPlan.objects.filter(tier='free').first() or 
                        SubscriptionPlan.objects.first()
            }
        )
        
        if created:
            # If we just created a subscription, set up trial
            subscription = Subscription.create_free_trial(tenant)
        
        return subscription


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_subscription(request):
    """Create or update a subscription."""
    
    serializer = SubscriptionCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Get tenant
        tenant = Tenant.objects.filter(owner=request.user).first()
        if not tenant:
            tenant = Tenant.objects.first()  # Fallback for development
        
        if not tenant:
            return Response(
                {'error': 'No tenant found for user'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        plan = SubscriptionPlan.objects.get(id=serializer.validated_data['plan_id'])
        
        # For demo purposes, create a local subscription without Stripe
        # In production, you would integrate with Stripe here
        subscription, created = Subscription.objects.get_or_create(
            tenant=tenant,
            defaults={'plan': plan}
        )
        
        if not created:
            # Update existing subscription
            subscription.plan = plan
            subscription.save()
        
        response_serializer = SubscriptionSerializer(subscription)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
        
    except SubscriptionPlan.DoesNotExist:
        return Response(
            {'error': 'Subscription plan not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_feature_access(request):
    """Check if current tenant has access to a feature."""
    
    feature_name = request.data.get('feature_name')
    if not feature_name:
        return Response(
            {'error': 'feature_name is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get tenant subscription
        tenant = Tenant.objects.filter(owner=request.user).first()
        if not tenant:
            tenant = Tenant.objects.first()  # Fallback for development
        
        if not tenant:
            return Response({
                'feature_name': feature_name,
                'has_access': False,
                'reason': 'No tenant found'
            })
        
        try:
            subscription = Subscription.objects.get(tenant=tenant)
        except Subscription.DoesNotExist:
            # Create trial subscription if none exists
            subscription = Subscription.create_free_trial(tenant)
        
        has_access = subscription.can_use_feature(feature_name)
        reason = ''
        
        if not has_access:
            if not subscription.is_active:
                reason = 'Subscription is not active'
            else:
                reason = 'Feature not included in current plan'
        
        return Response({
            'feature_name': feature_name,
            'has_access': has_access,
            'reason': reason,
            'subscription_status': subscription.status,
            'plan_name': subscription.plan.name
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscription_usage(request):
    """Get subscription usage statistics."""
    
    try:
        # Get tenant subscription
        tenant = Tenant.objects.filter(owner=request.user).first()
        if not tenant:
            tenant = Tenant.objects.first()  # Fallback for development
        
        if not tenant:
            return Response(
                {'error': 'No tenant found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            subscription = Subscription.objects.get(tenant=tenant)
        except Subscription.DoesNotExist:
            subscription = Subscription.create_free_trial(tenant)
        
        # Update usage counts from actual data
        from apps.suppliers.models import Supplier
        from apps.customers.models import Customer
        from apps.purchase_orders.models import PurchaseOrder
        from django.contrib.auth.models import User
        from django.utils import timezone
        from datetime import datetime
        
        # Count current usage
        subscription.current_suppliers = Supplier.objects.filter(tenant=tenant).count()
        subscription.current_customers = Customer.objects.filter(tenant=tenant).count()
        subscription.current_users = User.objects.filter(
            # In a real multi-tenant setup, you'd filter by tenant membership
        ).count()
        
        # Count this month's orders
        now = timezone.now()
        month_start = datetime(now.year, now.month, 1, tzinfo=now.tzinfo)
        subscription.current_month_orders = PurchaseOrder.objects.filter(
            tenant=tenant,
            created_on__gte=month_start
        ).count()
        
        subscription.save()
        
        usage_limits = subscription.check_usage_limits()
        
        return Response({
            'subscription': SubscriptionSerializer(subscription).data,
            'usage': {
                'users': subscription.current_users,
                'suppliers': subscription.current_suppliers,
                'customers': subscription.current_customers,
                'orders_this_month': subscription.current_month_orders,
            },
            'limits': {
                'users': subscription.plan.max_users,
                'suppliers': subscription.plan.max_suppliers,
                'customers': subscription.plan.max_customers,
                'orders_per_month': subscription.plan.max_orders_per_month,
            },
            'exceeded_limits': usage_limits
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class InvoiceListView(generics.ListAPIView):
    """List invoices for current tenant."""
    
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get invoices for current user's tenant."""
        tenant = Tenant.objects.filter(owner=self.request.user).first()
        if not tenant:
            tenant = Tenant.objects.first()  # Fallback for development
        
        if not tenant:
            return Invoice.objects.none()
        
        try:
            subscription = Subscription.objects.get(tenant=tenant)
            return Invoice.objects.filter(subscription=subscription)
        except Subscription.DoesNotExist:
            return Invoice.objects.none()
