"""
Carrier models for ProjectMeats.

Manages transportation carriers and logistics providers
for meat delivery in the brokerage system.
"""
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from apps.core.models import TenantOwnedModel, StatusModel


class CarrierType(models.TextChoices):
    """Types of carriers."""
    TRUCKING = "trucking", "Trucking Company"
    REFRIGERATED = "refrigerated", "Refrigerated Transport"
    LTL = "ltl", "Less Than Truckload (LTL)"
    FTL = "ftl", "Full Truckload (FTL)"
    LOCAL_DELIVERY = "local_delivery", "Local Delivery"
    COURIER = "courier", "Courier Service"


class Carrier(TenantOwnedModel, StatusModel):
    """Carrier model for managing transportation providers."""
    
    name = models.CharField(
        max_length=200,
        help_text="Carrier company name"
    )
    carrier_type = models.CharField(
        max_length=20,
        choices=CarrierType.choices,
        default=CarrierType.TRUCKING,
        help_text="Type of carrier service"
    )
    
    # Contact Information
    primary_contact = models.CharField(
        max_length=100,
        blank=True,
        help_text="Primary contact person name"
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        help_text="Primary email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        help_text="Primary phone number"
    )
    emergency_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        help_text="Emergency contact phone number"
    )
    
    # Address Information
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default="United States", blank=True)
    
    # Business Information
    dot_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="DOT (Department of Transportation) number"
    )
    mc_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="MC (Motor Carrier) number"
    )
    insurance_policy = models.CharField(
        max_length=100,
        blank=True,
        help_text="Insurance policy number"
    )
    website = models.URLField(blank=True)
    
    # Service Information
    service_areas = models.TextField(
        blank=True,
        help_text="Geographic areas served"
    )
    specializations = models.TextField(
        blank=True,
        help_text="Special services or equipment (temperature controlled, etc.)"
    )
    
    # Performance tracking
    preferred = models.BooleanField(
        default=False,
        help_text="Mark as preferred carrier"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Performance rating (1.00 - 5.00)"
    )
    
    notes = models.TextField(blank=True, help_text="Additional notes about the carrier")
    
    class Meta:
        db_table = "carriers"
        verbose_name = "Carrier"
        verbose_name_plural = "Carriers"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'name'],
                name='unique_carrier_name_per_tenant'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_carrier_type_display()})"

    @property
    def full_address(self):
        """Get formatted full address."""
        address_parts = [
            self.address_line1,
            self.address_line2,
            f"{self.city}, {self.state} {self.postal_code}".strip(" ,"),
            self.country
        ]
        return ", ".join(part for part in address_parts if part)