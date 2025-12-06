from django.core.management.base import BaseCommand
from apps.accounts.models import User
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Crea 200 usuarios de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        roles = [User.ESTANDAR, User.LEGAL, User.ADMINISTRADOR]
        
        created_count = 0
        
        for i in range(200):
            try:
                username = f"user_{i+1}_{fake.user_name()}"
                email = f"user_{i+1}@example.com"
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number()[:12],
                    role=random.choice(roles),
                    dni=fake.unique.numerify(text='########'),
                    saldo=round(random.uniform(50, 500), 2)
                )
                created_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creando usuario {i+1}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Se crearon {created_count} usuarios exitosamente')
        )
