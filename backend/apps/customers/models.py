"""
Customer models for ProjectMeats.

Manages customer relationships, order history, and business details
for meat purchasers in the brokerage system.
"""
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from apps.core.models import TenantOwnedModel, StatusModel


class CustomerType(models.TextChoices):
    """Types of customers."""
    RESTAURANT = "restaurant", "Restaurant"
    RETAILER = "retailer", "Retailer"
    FOODSERVICE = "foodservice", "Food Service"
    PROCESSOR = "processor", "Processor"
    DISTRIBUTOR = "distributor", "Distributor"
    INSTITUTION = "institution", "Institution"


class Customer(TenantOwnedModel, StatusModel):
    """Customer model for managing meat purchaser information."""
    
    name = models.CharField(
        max_length=200,
        help_text="Customer company name"
    )
    customer_type = models.CharField(
        max_length=20,
        choices=CustomerType.choices,
        default=CustomerType.RESTAURANT,
        help_text="Type of customer business"
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
    notes = models.TextField(blank=True, help_text="Additional notes about the customer")
    
    # Business relationship
    preferred = models.BooleanField(
        default=False,
        help_text="Mark as preferred customer"
    )
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Credit limit for this customer"
    )
    payment_terms = models.CharField(
        max_length=50,
        blank=True,
        help_text="Payment terms (e.g., Net 30, COD, etc.)"
    )
    
    class Meta:
        db_table = "customers"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'name'],
                name='unique_customer_name_per_tenant'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_customer_type_display()})"

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


class CustomerContact(TenantOwnedModel):
    """Additional contacts for customers."""
    
    customer = models.ForeignKey(
        Customer,
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
        db_table = "customer_contacts"
        verbose_name = "Customer Contact"
        verbose_name_plural = "Customer Contacts"
        ordering = ["-is_primary", "name"]

    def __str__(self):
        return f"{self.name} at {self.customer.name}"