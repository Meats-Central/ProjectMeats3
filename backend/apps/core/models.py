"""
Core models for ProjectMeats.

Provides base models and common functionality used across all apps.
"""
from django.contrib.auth.models import User
from django.db import models


class StatusChoices(models.TextChoices):
    """Common status choices for entities."""
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    ARCHIVED = "archived", "Archived"


class Tenant(models.Model):
    """Tenant model for multi-tenancy support."""
    
    name = models.CharField(
        max_length=100,
        help_text="Display name of the tenant organization"
    )
    subdomain = models.CharField(
        max_length=63,
        unique=True,
        help_text="Unique subdomain for the tenant (e.g., 'acme' for acme.projectmeats.com)"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Primary owner/admin of the tenant"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the tenant is active and can access the system"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "core_tenants"
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.subdomain})"


class StatusModel(models.Model):
    """Abstract base model for entities with status."""
    
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        help_text="Current status of the entity",
    )

    class Meta:
        abstract = True


class TimestampModel(models.Model):
    """Abstract base model for entities with timestamps."""
    
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnedModel(TimestampModel):
    """Abstract base model for entities with ownership."""
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who owns this entity",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_created",
        help_text="User who created this entity",
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_modified",
        help_text="User who last modified this entity",
    )

    class Meta:
        abstract = True


class TenantConfig(models.Model):
    """Configuration settings for tenant customization."""
    
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="config",
        help_text="Tenant this configuration belongs to"
    )
    
    # Theme and branding configuration
    theme_config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Theme configuration (colors, fonts, logos, etc.)"
    )
    
    # Feature toggles
    feature_flags = models.JSONField(
        default=dict,
        blank=True,
        help_text="Feature flag configuration for this tenant"
    )
    
    # Business settings
    business_settings = models.JSONField(
        default=dict,
        blank=True,
        help_text="Business-specific settings and preferences"
    )
    
    # Notification settings
    notification_settings = models.JSONField(
        default=dict,
        blank=True,
        help_text="Notification preferences and settings"
    )
    
    # Custom fields configuration
    custom_fields = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom field definitions for entities"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tenant_configs"
        verbose_name = "Tenant Configuration"
        verbose_name_plural = "Tenant Configurations"

    def __str__(self):
        return f"Config for {self.tenant.name}"

    def get_theme_setting(self, key, default=None):
        """Get a specific theme setting."""
        return self.theme_config.get(key, default)

    def get_feature_flag(self, flag_name, default=False):
        """Check if a feature flag is enabled."""
        return self.feature_flags.get(flag_name, default)

    def get_business_setting(self, key, default=None):
        """Get a specific business setting."""
        return self.business_settings.get(key, default)

    @classmethod
    def get_default_config(cls):
        """Get default configuration for new tenants."""
        return {
            'theme_config': {
                'primary_color': '#2563eb',
                'secondary_color': '#64748b',
                'accent_color': '#059669',
                'logo_url': '',
                'favicon_url': '',
                'font_family': 'Inter, system-ui, sans-serif',
                'custom_css': ''
            },
            'feature_flags': {
                'ai_assistant': True,
                'advanced_reporting': True,
                'document_processing': True,
                'multi_currency': False,
                'inventory_management': True,
                'mobile_app': True
            },
            'business_settings': {
                'default_currency': 'USD',
                'timezone': 'UTC',
                'date_format': 'MM/DD/YYYY',
                'number_format': 'US',
                'company_name': '',
                'company_address': '',
                'default_payment_terms': 'Net 30'
            },
            'notification_settings': {
                'email_notifications': True,
                'order_confirmations': True,
                'payment_reminders': True,
                'system_alerts': True,
                'marketing_emails': False
            }
        }


class TenantOwnedModel(TimestampModel):
    """Abstract base model for tenant-scoped entities with ownership."""
    
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,  # Temporary for migration
        blank=True,
        help_text="Tenant this entity belongs to"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who owns this entity",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_created",
        help_text="User who created this entity",
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_modified",
        help_text="User who last modified this entity",
    )

    class Meta:
        abstract = True