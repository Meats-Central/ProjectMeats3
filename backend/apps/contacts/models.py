"""
Contact models for ProjectMeats.

Manages general contacts and relationships in the brokerage system.
"""
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from apps.core.models import TenantOwnedModel, StatusModel


class ContactType(models.TextChoices):
    """Types of contacts."""
    CUSTOMER = "customer", "Customer Contact"
    SUPPLIER = "supplier", "Supplier Contact"
    CARRIER = "carrier", "Carrier/Logistics"
    INSPECTOR = "inspector", "Inspector"
    VENDOR = "vendor", "Vendor"
    PARTNER = "partner", "Business Partner"
    OTHER = "other", "Other"


class Contact(TenantOwnedModel, StatusModel):
    """General contact model for managing business contacts."""
    
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(
        max_length=100,
        blank=True,
        help_text="Job title or position"
    )
    
    # Contact Information
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        help_text="Email address"
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
    mobile_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        help_text="Mobile phone number"
    )
    
    # Business Information
    company = models.CharField(
        max_length=200,
        blank=True,
        help_text="Company name"
    )
    contact_type = models.CharField(
        max_length=20,
        choices=ContactType.choices,
        default=ContactType.OTHER,
        help_text="Type of contact relationship"
    )
    
    # Address Information
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default="United States", blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True, help_text="Additional notes about the contact")
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=[
            ("email", "Email"),
            ("phone", "Phone"),
            ("mobile", "Mobile"),
        ],
        default="email",
        help_text="Preferred method of contact"
    )
    
    # Relationships
    related_customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="related_contacts",
        help_text="Related customer if applicable"
    )
    related_supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="related_contacts",
        help_text="Related supplier if applicable"
    )
    
    class Meta:
        db_table = "contacts"
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}"
        if self.company:
            return f"{full_name} ({self.company})"
        return full_name

    @property
    def full_name(self):
        """Get full name."""
        return f"{self.first_name} {self.last_name}".strip()

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