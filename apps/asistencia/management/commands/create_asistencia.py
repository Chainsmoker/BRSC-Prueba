from django.core.management.base import BaseCommand
from apps.asistencia.models import Asistencia
from apps.accounts.models import User
from faker import Faker
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Crea 20 asistencias para cada usuario'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(
                self.style.ERROR('No hay usuarios en la base de datos')
            )
            return
        
        created_count = 0
        
        for user in users:
            for i in range(20):
                try:
                    fecha = fake.date_between(start_date='-60d', end_date='today')
                    
                    hora_entrada = datetime.strptime(f"{random.randint(7, 9)}:{random.randint(0, 59):02d}", "%H:%M").time()
                    
                    horas_trabajo = random.randint(7, 10)
                    minutos_trabajo = random.randint(0, 59)
                    
                    entrada_dt = datetime.combine(fecha, hora_entrada)
                    salida_dt = entrada_dt + timedelta(hours=horas_trabajo, minutes=minutos_trabajo)
                    hora_salida = salida_dt.time()
                    
                    horas_trabajadas = datetime.strptime(f"{horas_trabajo}:{minutos_trabajo:02d}", "%H:%M").time()
                    
                    Asistencia.objects.create(
                        trabajador=user,
                        fecha=fecha,
                        entrada=hora_entrada,
                        salida=hora_salida,
                        horas_trabajadas=horas_trabajadas
                    )
                    created_count += 1
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creando asistencia para {user.username}: {str(e)}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'Se crearon {created_count} asistencias exitosamente')
        )
