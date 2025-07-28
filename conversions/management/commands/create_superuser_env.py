"""
Django management command to create a superuser with environment variables.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with environment variables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Superuser username',
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Superuser email',
            default=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@fileconvert.com')
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Superuser password',
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123456')
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists.')
                )
                return

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Username: {username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {email}')
            )
            self.stdout.write(
                self.style.WARNING('Please change the default password after first login!')
            )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )
