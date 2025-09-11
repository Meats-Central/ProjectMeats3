"""
Serializers for core models.
"""
from rest_framework import serializers
from .models import Tenant, TenantConfig


class TenantSerializer(serializers.ModelSerializer):
    """Serializer for Tenant model."""
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'subdomain', 'owner', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']


class TenantConfigSerializer(serializers.ModelSerializer):
    """Serializer for TenantConfig model."""
    
    class Meta:
        model = TenantConfig
        fields = [
            'tenant', 'theme_config', 'feature_flags', 'business_settings',
            'notification_settings', 'custom_fields', 'created_at', 'updated_at'
        ]
        read_only_fields = ['tenant', 'created_at', 'updated_at']

    def validate_theme_config(self, value):
        """Validate theme configuration."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Theme config must be a JSON object")
        return value

    def validate_feature_flags(self, value):
        """Validate feature flags."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Feature flags must be a JSON object")
        return value