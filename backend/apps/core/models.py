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