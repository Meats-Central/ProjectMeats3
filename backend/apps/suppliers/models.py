"""
Supplier models for ProjectMeats.

Manages supplier relationships, contact information, and business details
for meat suppliers in the brokerage system.
"""
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from apps.core.models import TenantOwnedModel, StatusModel


class SupplierType(models.TextChoices):
    """Types of meat suppliers."""
    PROCESSOR = "processor", "Meat Processor"
    PACKER = "packer", "Meat Packer"
    DISTRIBUTOR = "distributor", "Distributor"
    FARM = "farm", "Farm/Ranch"
    WHOLESALER = "wholesaler", "Wholesaler"


class Supplier(TenantOwnedModel, StatusModel):
    """Supplier model for managing meat supplier information."""
    
    name = models.CharField(
        max_length=200,
        help_text="Supplier company name"
    )
    supplier_type = models.CharField(
        max_length=20,
        choices=SupplierType.choices,
        default=SupplierType.PROCESSOR,
        help_text="Type of supplier operation"
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
    
    # Address Information
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default="United States", blank=True)
    
    # Business Information
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Tax identification number"
    )
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True, help_text="Additional notes about the supplier")
    
    # Performance tracking
    preferred = models.BooleanField(
        default=False,
        help_text="Mark as preferred supplier"
    )
    credit_rating = models.CharField(
        max_length=10,
        blank=True,
        help_text="Credit rating (e.g., AAA, AA, A, B, C)"
    )
    
    class Meta:
        db_table = "suppliers"
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'name'],
                name='unique_supplier_name_per_tenant'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_supplier_type_display()})"

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


class SupplierContact(TenantOwnedModel):
    """Additional contacts for suppliers."""
    
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="contacts"
    )
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, validators=[EmailValidator()])
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = "supplier_contacts"
        verbose_name = "Supplier Contact"
        verbose_name_plural = "Supplier Contacts"
        ordering = ["-is_primary", "name"]

    def __str__(self):
        return f"{self.name} at {self.supplier.name}"