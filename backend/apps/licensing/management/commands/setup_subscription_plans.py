"""
Management command to create default subscription plans.
"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.licensing.models import SubscriptionPlan, PlanTier


class Command(BaseCommand):
    help = 'Create default subscription plans for SaaS platform'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Free Plan
                free_plan, created = SubscriptionPlan.objects.get_or_create(
                    name='Free Trial',
                    tier=PlanTier.FREE,
                    defaults={
                        'monthly_price': Decimal('0.00'),
                        'yearly_price': Decimal('0.00'),
                        'max_users': 2,
                        'max_suppliers': 5,
                        'max_customers': 10,
                        'max_orders_per_month': 25,
                        'has_ai_assistant': True,
                        'has_advanced_reporting': False,
                        'has_document_processing': True,
                        'has_api_access': False,
                        'has_priority_support': False,
                        'has_custom_branding': False,
                        'description': 'Perfect for trying out ProjectMeats with basic features',
                        'features': [
                            'Up to 2 users',
                            'Up to 5 suppliers',
                            'Up to 10 customers', 
                            'Up to 25 orders per month',
                            'Basic AI assistant',
                            'Document processing',
                            'Standard support'
                        ]
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created plan: {free_plan.name}')
                    )

                # Basic Plan
                basic_plan, created = SubscriptionPlan.objects.get_or_create(
                    name='Basic',
                    tier=PlanTier.BASIC,
                    defaults={
                        'monthly_price': Decimal('29.00'),
                        'yearly_price': Decimal('290.00'),  # 2 months free
                        'max_users': 5,
                        'max_suppliers': 25,
                        'max_customers': 50,
                        'max_orders_per_month': 100,
                        'has_ai_assistant': True,
                        'has_advanced_reporting': True,
                        'has_document_processing': True,
                        'has_api_access': False,
                        'has_priority_support': False,
                        'has_custom_branding': False,
                        'description': 'Great for small businesses getting started',
                        'features': [
                            'Up to 5 users',
                            'Up to 25 suppliers',
                            'Up to 50 customers',
                            'Up to 100 orders per month',
                            'Full AI assistant',
                            'Advanced reporting',
                            'Document processing',
                            'Email support'
                        ]
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created plan: {basic_plan.name}')
                    )

                # Professional Plan
                pro_plan, created = SubscriptionPlan.objects.get_or_create(
                    name='Professional',
                    tier=PlanTier.PROFESSIONAL,
                    defaults={
                        'monthly_price': Decimal('79.00'),
                        'yearly_price': Decimal('790.00'),  # 2 months free
                        'max_users': 15,
                        'max_suppliers': 100,
                        'max_customers': 200,
                        'max_orders_per_month': 500,
                        'has_ai_assistant': True,
                        'has_advanced_reporting': True,
                        'has_document_processing': True,
                        'has_api_access': True,
                        'has_priority_support': True,
                        'has_custom_branding': True,
                        'description': 'Perfect for growing businesses with advanced needs',
                        'features': [
                            'Up to 15 users',
                            'Up to 100 suppliers',
                            'Up to 200 customers',
                            'Up to 500 orders per month',
                            'Full AI assistant',
                            'Advanced reporting & analytics',
                            'Document processing',
                            'API access',
                            'Custom branding',
                            'Priority support'
                        ]
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created plan: {pro_plan.name}')
                    )

                # Enterprise Plan
                enterprise_plan, created = SubscriptionPlan.objects.get_or_create(
                    name='Enterprise',
                    tier=PlanTier.ENTERPRISE,
                    defaults={
                        'monthly_price': Decimal('199.00'),
                        'yearly_price': Decimal('1990.00'),  # 2 months free
                        'max_users': None,  # Unlimited
                        'max_suppliers': None,  # Unlimited
                        'max_customers': None,  # Unlimited
                        'max_orders_per_month': None,  # Unlimited
                        'has_ai_assistant': True,
                        'has_advanced_reporting': True,
                        'has_document_processing': True,
                        'has_api_access': True,
                        'has_priority_support': True,
                        'has_custom_branding': True,
                        'description': 'For large enterprises with unlimited needs',
                        'features': [
                            'Unlimited users',
                            'Unlimited suppliers',
                            'Unlimited customers',
                            'Unlimited orders',
                            'Full AI assistant',
                            'Advanced reporting & analytics',
                            'Document processing',
                            'Full API access',
                            'Custom branding',
                            'Priority support',
                            'Custom integrations',
                            'Dedicated account manager'
                        ]
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created plan: {enterprise_plan.name}')
                    )

                # Show plan summary
                plans = SubscriptionPlan.objects.filter(is_active=True).order_by('monthly_price')
                
                self.stdout.write(
                    self.style.SUCCESS(f'\n🎉 Subscription plans setup completed!')
                )
                
                self.stdout.write('\n📊 Available Plans:')
                for plan in plans:
                    discount = plan.yearly_discount if plan.yearly_discount else 0
                    self.stdout.write(
                        f'  • {plan.name} - ${plan.monthly_price}/month'
                        + (f' (${plan.yearly_price}/year, {discount:.0f}% discount)' if plan.yearly_price else '')
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating subscription plans: {str(e)}')
            )
            raise