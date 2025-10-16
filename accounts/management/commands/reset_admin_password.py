from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Reset admin password'

    def add_arguments(self, parser):
        parser.add_argument('--password', type=str, help='New password for admin')

    def handle(self, *args, **options):
        password = options.get('password')
        
        if not password:
            password = input('Enter new password for admin: ')
        
        try:
            admin_user = CustomUser.objects.get(email='admin@didactia.com')
            admin_user.set_password(password)
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated password for {admin_user.email}')
            )
        except CustomUser.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Admin user with email admin@didactia.com not found')
            )