"""
Management command to create a default tenant and sample data for testing.
"""
import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import Tenant
from apps.suppliers.models import Supplier, SupplierType
from apps.customers.models import Customer, CustomerType


class Command(BaseCommand):
    help = 'Create default tenant and sample data for SaaS development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tenant-name',
            type=str,
            default='Default Tenant',
            help='Name of the default tenant'
        )
        parser.add_argument(
            '--subdomain',
            type=str,
            default='default',
            help='Subdomain for the default tenant'
        )

    def handle(self, *args, **options):
        tenant_name = options['tenant_name']
        subdomain = options['subdomain']

        try:
            with transaction.atomic():
                # Get or create admin user
                admin_user, created = User.objects.get_or_create(
                    username='admin',
                    defaults={
                        'email': 'admin@projectmeats.com',
                        'is_staff': True,
                        'is_superuser': True,
                        'first_name': 'Project',
                        'last_name': 'Admin'
                    }
                )
                
                if created:
                    admin_user.set_password('WATERMELON1219')
                    admin_user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created admin user: {admin_user.username}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Admin user already exists: {admin_user.username}')
                    )

                # Create default tenant
                tenant, created = Tenant.objects.get_or_create(
                    subdomain=subdomain,
                    defaults={
                        'name': tenant_name,
                        'owner': admin_user,
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created default tenant: {tenant.name} ({tenant.subdomain})')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Default tenant already exists: {tenant.name}')
                    )

                # Create sample suppliers
                sample_suppliers = [
                    {
                        'name': 'Premium Meats Co.',
                        'supplier_type': SupplierType.PROCESSOR,
                        'email': 'contact@premiummeats.com',
                        'phone': '+1-555-0101',
                        'city': 'Chicago',
                        'state': 'IL'
                    },
                    {
                        'name': 'Midwest Livestock',
                        'supplier_type': SupplierType.FARM,
                        'email': 'info@midwestlivestock.com',
                        'phone': '+1-555-0102',
                        'city': 'Des Moines',
                        'state': 'IA'
                    }
                ]

                for supplier_data in sample_suppliers:
                    supplier, created = Supplier.objects.get_or_create(
                        name=supplier_data['name'],
                        tenant=tenant,
                        defaults={
                            **supplier_data,
                            'owner': admin_user,
                            'created_by': admin_user,
                            'modified_by': admin_user
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created supplier: {supplier.name}')
                        )

                # Create sample customers
                sample_customers = [
                    {
                        'name': 'Fine Dining Restaurant Group',
                        'customer_type': CustomerType.RESTAURANT,
                        'email': 'orders@finedining.com',
                        'phone': '+1-555-0201',
                        'city': 'New York',
                        'state': 'NY'
                    },
                    {
                        'name': 'Metro Food Service',
                        'customer_type': CustomerType.FOODSERVICE,
                        'email': 'purchasing@metrofood.com',
                        'phone': '+1-555-0202',
                        'city': 'Los Angeles',
                        'state': 'CA'
                    }
                ]

                for customer_data in sample_customers:
                    customer, created = Customer.objects.get_or_create(
                        name=customer_data['name'],
                        tenant=tenant,
                        defaults={
                            **customer_data,
                            'owner': admin_user,
                            'created_by': admin_user,
                            'modified_by': admin_user
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created customer: {customer.name}')
                        )

                # Update AI Assistant models if they exist but don't have tenants
                from apps.ai_assistant.models import ChatSession, ChatMessage
                
                sessions_updated = ChatSession.objects.filter(tenant__isnull=True).update(tenant=tenant)
                messages_updated = ChatMessage.objects.filter(tenant__isnull=True).update(tenant=tenant)
                
                if sessions_updated:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated {sessions_updated} chat sessions with tenant')
                    )
                if messages_updated:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated {messages_updated} chat messages with tenant')
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n🎉 Default tenant setup completed successfully!\n'
                        f'Tenant: {tenant.name} ({tenant.subdomain})\n'
                        f'Admin: {admin_user.username}\n'
                        f'Login at: http://localhost:8000/admin/\n'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating default tenant: {str(e)}')
            )
            raise