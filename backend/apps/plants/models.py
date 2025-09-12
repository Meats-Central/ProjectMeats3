"""
Plant models for ProjectMeats.

Manages meat processing plants, facilities, and plant information
in the brokerage system.
"""
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from apps.core.models import TenantOwnedModel, StatusModel


class PlantType(models.TextChoices):
    """Types of meat processing plants."""
    SLAUGHTER = "slaughter", "Slaughter Facility"
    PROCESSING = "processing", "Processing Plant"
    PACKAGING = "packaging", "Packaging Facility"
    COLD_STORAGE = "cold_storage", "Cold Storage"
    DISTRIBUTION = "distribution", "Distribution Center"


class CertificationType(models.TextChoices):
    """Certification types for plants."""
    USDA = "usda", "USDA Inspected"
    ORGANIC = "organic", "USDA Organic"
    HALAL = "halal", "Halal Certified"
    KOSHER = "kosher", "Kosher Certified"
    SQF = "sqf", "SQF Certified"
    BRC = "brc", "BRC Certified"
    HACCP = "haccp", "HACCP Certified"


class Plant(TenantOwnedModel, StatusModel):
    """Plant model for managing meat processing facilities."""
    
    name = models.CharField(
        max_length=200,
        help_text="Plant/facility name"
    )
    plant_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Official plant number (e.g., USDA establishment number)"
    )
    plant_type = models.CharField(
        max_length=20,
        choices=PlantType.choices,
        default=PlantType.PROCESSING,
        help_text="Type of processing plant"
    )
    
    # Contact Information
    manager_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Plant manager name"
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        help_text="Plant email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        help_text="Plant phone number"
    )
    
    # Address Information
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default="United States", blank=True)
    
    # Capacity and Operations
    daily_capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Daily processing capacity (in pounds or heads)"
    )
    capacity_unit = models.CharField(
        max_length=20,
        default="lbs",
        help_text="Unit for capacity measurement"
    )
    operating_days = models.CharField(
        max_length=50,
        blank=True,
        help_text="Operating days/schedule"
    )
    
    # Additional Information
    notes = models.TextField(blank=True, help_text="Additional notes about the plant")
    website = models.URLField(blank=True)
    
    class Meta:
        db_table = "plants"
        verbose_name = "Plant"
        verbose_name_plural = "Plants"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'name'],
                name='unique_plant_name_per_tenant'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_plant_type_display()})"

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


class PlantCertification(TenantOwnedModel):
    """Certifications for plants."""
    
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="certifications"
    )
    certification_type = models.CharField(
        max_length=20,
        choices=CertificationType.choices,
        help_text="Type of certification"
    )
    certification_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Certification number/identifier"
    )
    issued_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date certification was issued"
    )
    expiration_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date certification expires"
    )
    issuing_body = models.CharField(
        max_length=200,
        blank=True,
        help_text="Organization that issued the certification"
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = "plant_certifications"
        verbose_name = "Plant Certification"
        verbose_name_plural = "Plant Certifications"
        ordering = ["-issued_date"]

    def __str__(self):
        return f"{self.plant.name} - {self.get_certification_type_display()}"

    @property
    def is_expired(self):
        """Check if certification is expired."""
        if not self.expiration_date:
            return False
        from django.utils import timezone
        return self.expiration_date < timezone.now().date()