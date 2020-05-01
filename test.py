from django.core.management import call_command
from apps.b3_tests.testcases.common_testcases import TestCase


class CallManagementCommandTest(TestCase):
    apps_to_replace = [
        'address',
        'b3_address',
        'b3_api',
        'b3_attachement',
        'b3_auth_plugins',
        'b3_calendar',
        'b3_checkout',
        'b3_comment',
        'b3_compare',
        'b3_core',
        'b3_impersonate',
        'b3_machine',
        'b3_manual_request',
        'b3_mes',
        'b3_migration',
        'b3_misc',
        'b3_modal',
        'b3_obfuscation',
        'b3_order',
        'b3_organization',
        'b3_pdf',
        'b3_shipping',
        'b3_signup',
        'b3_tests',
        'b3_user_panel',
        'b3_voucher',
        'basket',
        'catalogue',
        'customer',
        'django_replace_migrations',
        'offer',
        'order',
        'partner',
        'payment',
        'shipping',
        'status_page',
        'voucher',
    ]
    def test_command(self):
        call_command('makemigrations', *self.apps_to_replace,
                     replace_all=True, name='replaces-3-7-0'
                     )
