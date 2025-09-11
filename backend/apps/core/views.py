"""
API views for core models.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Tenant, TenantConfig
from .serializers import TenantSerializer, TenantConfigSerializer


class TenantListCreateView(generics.ListCreateAPIView):
    """List tenants or create a new tenant (admin only)."""
    
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        """Set the current user as the tenant owner."""
        tenant = serializer.save(owner=self.request.user)
        
        # Create default configuration for the new tenant
        TenantConfig.objects.create(
            tenant=tenant,
            **TenantConfig.get_default_config()
        )


class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a tenant (admin only)."""
    
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def tenant_config_view(request):
    """Get or update tenant configuration for the current user's tenant."""
    
    # For now, we'll assume the user belongs to the first tenant
    # In a real multi-tenant setup, this would be determined by middleware
    try:
        # Get the tenant from the user's ownership or first available
        tenant = Tenant.objects.filter(owner=request.user).first()
        if not tenant:
            tenant = Tenant.objects.first()  # Fallback for development
        
        if not tenant:
            return Response(
                {'error': 'No tenant found for user'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get or create tenant configuration
        config, created = TenantConfig.objects.get_or_create(
            tenant=tenant,
            defaults=TenantConfig.get_default_config()
        )
        
        if request.method == 'GET':
            serializer = TenantConfigSerializer(config)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = TenantConfigSerializer(
                config, 
                data=request.data, 
                partial=partial
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def tenant_theme_view(request):
    """Get theme configuration for the current tenant."""
    
    try:
        # Get the tenant (same logic as above)
        tenant = Tenant.objects.filter(owner=request.user).first()
        if not tenant:
            tenant = Tenant.objects.first()
        
        if not tenant:
            return Response(
                {'error': 'No tenant found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        config, created = TenantConfig.objects.get_or_create(
            tenant=tenant,
            defaults=TenantConfig.get_default_config()
        )
        
        return Response({
            'tenant': tenant.name,
            'subdomain': tenant.subdomain,
            'theme': config.theme_config,
            'features': config.feature_flags,
            'business': config.business_settings
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )