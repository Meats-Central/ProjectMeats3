"""
Accounts Receivable models for ProjectMeats.

Manages customer payments, invoices, and financial tracking
in the brokerage system.
"""
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TenantOwnedModel, StatusModel


class InvoiceStatus(models.TextChoices):
    """Status choices for invoices."""
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    CANCELLED = "cancelled", "Cancelled"


class PaymentStatus(models.TextChoices):
    """Status choices for payments."""
    PENDING = "pending", "Pending"
    PROCESSED = "processed", "Processed"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class AccountsReceivable(TenantOwnedModel, StatusModel):
    """Accounts receivable model for managing customer invoices."""
    
    invoice_number = models.CharField(
        max_length=50,
        help_text="Invoice number/identifier"
    )
    
    # Relationships
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name="invoices",
        help_text="Customer for this invoice"
    )
    purchase_order = models.ForeignKey(
        'purchase_orders.PurchaseOrder',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="invoices",
        help_text="Related purchase order if applicable"
    )
    
    # Invoice Information
    invoice_date = models.DateField(help_text="Date invoice was created")
    due_date = models.DateField(help_text="Payment due date")
    invoice_status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,
        help_text="Current status of the invoice"
    )
    
    # Financial Information
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Subtotal before taxes"
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.0000'),
        help_text="Tax rate as decimal (e.g., 0.0825 for 8.25%)"
    )
    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Tax amount"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total invoice amount"
    )
    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Amount paid so far"
    )
    
    # Additional Information
    notes = models.TextField(blank=True, help_text="Additional notes for the invoice")
    payment_terms = models.CharField(
        max_length=50,
        blank=True,
        help_text="Payment terms for this invoice"
    )
    
    class Meta:
        db_table = "accounts_receivables"
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ["-invoice_date"]
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'invoice_number'],
                name='unique_invoice_number_per_tenant'
            )
        ]

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.name}"

    @property
    def remaining_balance(self):
        """Calculate remaining balance."""
        return self.total_amount - self.paid_amount

    @property
    def is_overdue(self):
        """Check if invoice is overdue."""
        from django.utils import timezone
        return (
            self.due_date < timezone.now().date() 
            and self.remaining_balance > 0
            and self.invoice_status != InvoiceStatus.CANCELLED
        )

    @property
    def is_paid(self):
        """Check if invoice is fully paid."""
        return self.paid_amount >= self.total_amount

    def calculate_tax(self):
        """Calculate tax amount based on subtotal and tax rate."""
        self.tax_amount = self.subtotal * self.tax_rate
        self.total_amount = self.subtotal + self.tax_amount

    def save(self, *args, **kwargs):
        """Calculate tax and totals before saving."""
        self.calculate_tax()
        super().save(*args, **kwargs)


class Payment(TenantOwnedModel):
    """Payment model for tracking customer payments."""
    
    invoice = models.ForeignKey(
        AccountsReceivable,
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="Invoice this payment is for"
    )
    
    payment_date = models.DateField(help_text="Date payment was made")
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Payment amount"
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("cash", "Cash"),
            ("check", "Check"),
            ("credit_card", "Credit Card"),
            ("bank_transfer", "Bank Transfer"),
            ("ach", "ACH"),
            ("other", "Other"),
        ],
        default="check",
        help_text="Method of payment"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text="Status of the payment"
    )
    
    # Payment Details
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Check number, transaction ID, etc."
    )
    notes = models.TextField(blank=True, help_text="Additional notes about the payment")
    
    class Meta:
        db_table = "payments"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"${self.amount} payment for {self.invoice.invoice_number}"

    def save(self, *args, **kwargs):
        """Update invoice paid amount when payment is saved."""
        super().save(*args, **kwargs)
        
        # Update invoice paid amount
        if self.invoice_id:
            total_paid = self.invoice.payments.filter(
                payment_status=PaymentStatus.PROCESSED
            ).aggregate(
                total=models.Sum('amount')
            )['total'] or Decimal('0.00')
            
            self.invoice.paid_amount = total_paid
            
            # Update invoice status based on payment
            if self.invoice.is_paid:
                self.invoice.invoice_status = InvoiceStatus.PAID
            elif self.invoice.is_overdue:
                self.invoice.invoice_status = InvoiceStatus.OVERDUE
            
            self.invoice.save()