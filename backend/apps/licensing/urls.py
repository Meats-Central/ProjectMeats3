"""
URL configuration for licensing app.
"""
from django.urls import path
from .views import (
    SubscriptionPlanListView,
    SubscriptionDetailView,
    InvoiceListView,
    create_subscription,
    check_feature_access,
    subscription_usage,
)

urlpatterns = [
    path('subscription-plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('subscription/', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscription/create/', create_subscription, name='create-subscription'),
    path('subscription/usage/', subscription_usage, name='subscription-usage'),
    path('feature-access/', check_feature_access, name='check-feature-access'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
]