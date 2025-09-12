from django.urls import path
from .views import (
    TenantListCreateView,
    TenantDetailView,
    tenant_config_view,
    tenant_theme_view
)

urlpatterns = [
    path('tenants/', TenantListCreateView.as_view(), name='tenant-list-create'),
    path('tenants/<int:pk>/', TenantDetailView.as_view(), name='tenant-detail'),
    path('tenant-config/', tenant_config_view, name='tenant-config'),
    path('tenant-theme/', tenant_theme_view, name='tenant-theme'),
]