"""
Purchase Order models for ProjectMeats.

Manages purchase orders, order items, and order tracking
for meat transactions in the brokerage system.
"""
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TenantOwnedModel, StatusModel


class OrderStatus(models.TextChoices):
    """Status choices for purchase orders."""
    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending Approval"
    CONFIRMED = "confirmed", "Confirmed"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"
    COMPLETED = "completed", "Completed"


class PurchaseOrder(TenantOwnedModel, StatusModel):
    """Purchase order model for managing meat transactions."""
    
    po_number = models.CharField(
        max_length=50,
        help_text="Purchase order number/identifier"
    )
    
    # Relationships
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        related_name="purchase_orders",
        help_text="Supplier for this purchase order"
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name="purchase_orders",
        help_text="Customer for this purchase order"
    )
    
    # Order Information
    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.DRAFT,
        help_text="Current status of the purchase order"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    requested_delivery_date = models.DateField(
        null=True,
        blank=True,
        help_text="Requested delivery date"
    )
    actual_delivery_date = models.DateField(
        null=True,
        blank=True,
        help_text="Actual delivery date"
    )
    
    # Financial Information
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Subtotal before taxes and fees"
    )
    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Tax amount"
    )
    shipping_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Shipping/delivery cost"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Total order amount"
    )
    
    # Additional Information
    notes = models.TextField(blank=True, help_text="Additional notes for the order")
    internal_notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to customer/supplier)"
    )
    
    # Delivery Information
    delivery_address = models.TextField(
        blank=True,
        help_text="Delivery address if different from customer address"
    )
    special_instructions = models.TextField(
        blank=True,
        help_text="Special delivery or handling instructions"
    )
    
    class Meta:
        db_table = "purchase_orders"
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"
        ordering = ["-order_date"]
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'po_number'],
                name='unique_po_number_per_tenant'
            )
        ]

    def __str__(self):
        return f"PO {self.po_number} - {self.customer.name}"

    def calculate_totals(self):
        """Calculate and update order totals based on order items."""
        items = self.items.all()
        self.subtotal = sum(item.total_price for item in items)
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost
        self.save()

    @property
    def is_overdue(self):
        """Check if order is overdue based on requested delivery date."""
        if not self.requested_delivery_date:
            return False
        from django.utils import timezone
        return (
            self.requested_delivery_date < timezone.now().date() 
            and self.order_status not in [OrderStatus.DELIVERED, OrderStatus.COMPLETED, OrderStatus.CANCELLED]
        )


class MeatCut(models.TextChoices):
    """Common meat cuts and products."""
    RIBEYE = "ribeye", "Ribeye"
    STRIP = "strip", "Strip Steak"
    TENDERLOIN = "tenderloin", "Tenderloin"
    SIRLOIN = "sirloin", "Sirloin"
    CHUCK = "chuck", "Chuck"
    BRISKET = "brisket", "Brisket"
    GROUND_BEEF = "ground_beef", "Ground Beef"
    PORK_CHOP = "pork_chop", "Pork Chop"
    PORK_TENDERLOIN = "pork_tenderloin", "Pork Tenderloin"
    BACON = "bacon", "Bacon"
    HAM = "ham", "Ham"
    CHICKEN_BREAST = "chicken_breast", "Chicken Breast"
    CHICKEN_THIGH = "chicken_thigh", "Chicken Thigh"
    WHOLE_CHICKEN = "whole_chicken", "Whole Chicken"
    OTHER = "other", "Other"


class OrderItem(TenantOwnedModel):
    """Individual items within a purchase order."""
    
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )
    
    # Product Information
    product_name = models.CharField(
        max_length=200,
        help_text="Name/description of the meat product"
    )
    meat_cut = models.CharField(
        max_length=20,
        choices=MeatCut.choices,
        default=MeatCut.OTHER,
        help_text="Type of meat cut"
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        help_text="Meat grade (e.g., USDA Prime, Choice, Select)"
    )
    
    # Quantity and Pricing
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        help_text="Quantity ordered"
    )
    unit = models.CharField(
        max_length=20,
        default="lb",
        help_text="Unit of measurement (lb, kg, case, etc.)"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))],
        help_text="Price per unit"
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Total price for this line item"
    )
    
    # Additional Information
    notes = models.TextField(blank=True, help_text="Notes for this specific item")
    
    class Meta:
        db_table = "purchase_order_items"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["id"]

    def __str__(self):
        return f"{self.product_name} - {self.quantity} {self.unit}"

    def save(self, *args, **kwargs):
        """Calculate total price before saving."""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # Update parent order totals
        if self.purchase_order_id:
            self.purchase_order.calculate_totals()