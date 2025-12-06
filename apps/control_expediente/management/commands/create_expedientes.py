from django.core.management.base import BaseCommand
from apps.control_expediente.models import (
    CasoJudicial, Seguimiento, Gasto,
    CarpetaFiscal, SeguimientoFiscal, GastoFiscal,
    RegistroActividad
)
from apps.accounts.models import User
from faker import Faker
from datetime import timedelta
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Crea datos de prueba para expedientes'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        usuarios_legales = User.objects.filter(role=User.LEGAL)
        if not usuarios_legales.exists():
            usuarios_legales = User.objects.all()[:10]
        
        representantes = ['Demandante', 'Demandado', 'Martillero']
        estados = ['En proceso', 'Finalizado', 'Presentado', 'Notificado', 'Otros']
        materias = ['Civil', 'Laboral', 'Familia', 'Contencioso Administrativo', 'Comercial']
        especialidades = ['Civil', 'Penal', 'Laboral', 'Familia', 'Comercial']
        delitos = ['Estafa', 'Apropiación Ilícita', 'Falsificación', 'Robo', 'Hurto']
        
        casos_judiciales = []
        for i in range(50):
            caso = CasoJudicial.objects.create(
                codigo=fake.bothify(text='COD-####-????'),
                fecha_compromiso=fake.date_between(start_date='-1y', end_date='+30d'),
                expediente=fake.numerify(text='#####-####-####-####'),
                materia=random.choice(materias),
                juzgado=f"{fake.city()} - {random.randint(1, 20)}° Juzgado",
                demandante=fake.company(),
                demandado=fake.name(),
                sede=fake.city(),
                especialidad=random.choice(especialidades),
                representante=random.choice(representantes),
                pendiente=fake.text(max_nb_chars=200),
                concluido=random.choice([True, False]),
                responsable=random.choice(usuarios_legales) if usuarios_legales else None
            )
            casos_judiciales.append(caso)
        
        for caso in casos_judiciales:
            num_seguimientos = random.randint(2, 8)
            for j in range(num_seguimientos):
                fecha_seg = fake.date_between(start_date='-1y', end_date='today')
                seguimiento = Seguimiento.objects.create(
                    caso=caso,
                    resolucion=fake.bothify(text='RES-####-????'),
                    fecha_seguimiento=fecha_seg,
                    seguimiento=fake.text(max_nb_chars=300),
                    fecha_pendiente=fake.date_between(start_date='today', end_date='+60d'),
                    pendiente=fake.text(max_nb_chars=200),
                    responsable=fake.name(),
                    estado=random.choice(estados),
                    editor=fake.name(),
                    usuario=random.choice(usuarios_legales) if usuarios_legales else None,
                    fecha_alerta=fake.date_between(start_date='today', end_date='+45d')
                )
                
                if random.choice([True, False]):
                    Gasto.objects.create(
                        seguimiento=seguimiento,
                        fecha=fake.date_between(start_date='-6m', end_date='today'),
                        detalle=fake.sentence(nb_words=6),
                        sustento=fake.text(max_nb_chars=150),
                        codigo_pago=fake.bothify(text='PAG-########'),
                        gastos_soles=Decimal(str(round(random.uniform(50, 2000), 2))) if random.choice([True, False]) else None,
                        gastos_dolares=Decimal(str(round(random.uniform(10, 500), 2))) if random.choice([True, False]) else None,
                        editor=fake.name()
                    )
        
        carpetas_fiscales = []
        for i in range(30):
            carpeta = CarpetaFiscal.objects.create(
                item=fake.bothify(text='ITEM-###'),
                carpeta_fiscal=fake.numerify(text='####-####-####'),
                delito=random.choice(delitos),
                fiscalia=f"Fiscalía {fake.city()}",
                demandante=fake.company(),
                demandado=fake.name(),
                sede=fake.city(),
                especialidad='Penal',
                representante=random.choice(representantes),
                pendiente=fake.text(max_nb_chars=200),
                concluido=random.choice([True, False]),
                responsable=random.choice(usuarios_legales) if usuarios_legales else None
            )
            carpetas_fiscales.append(carpeta)
        
        for carpeta in carpetas_fiscales:
            num_seguimientos = random.randint(2, 6)
            for j in range(num_seguimientos):
                seguimiento_fiscal = SeguimientoFiscal.objects.create(
                    caso=carpeta,
                    resolucion=fake.bothify(text='RES-####-????'),
                    fecha_seguimiento=fake.date_between(start_date='-1y', end_date='today'),
                    seguimiento=fake.text(max_nb_chars=300),
                    fecha_pendiente=fake.date_between(start_date='today', end_date='+60d'),
                    pendiente=fake.text(max_nb_chars=200),
                    responsable=fake.name(),
                    estado=random.choice(estados),
                    inter=random.choice([True, False]),
                    editor=fake.name(),
                    usuario=random.choice(usuarios_legales) if usuarios_legales else None,
                    fecha_alerta=fake.date_between(start_date='today', end_date='+45d')
                )
                
                if random.choice([True, False]):
                    GastoFiscal.objects.create(
                        seguimiento=seguimiento_fiscal,
                        fecha=fake.date_between(start_date='-6m', end_date='today'),
                        detalle=fake.sentence(nb_words=6),
                        sustento=fake.text(max_nb_chars=150),
                        codigo_pago=fake.bothify(text='PAG-########'),
                        gastos_soles=Decimal(str(round(random.uniform(50, 2000), 2))) if random.choice([True, False]) else None,
                        gastos_dolares=Decimal(str(round(random.uniform(10, 500), 2))) if random.choice([True, False]) else None,
                        editor=fake.name()
                    )
        
        if usuarios_legales:
            for i in range(100):
                RegistroActividad.objects.create(
                    nombre=fake.name(),
                    fecha=fake.date_time_between(start_date='-6m', end_date='now'),
                    actividad=fake.sentence(nb_words=10),
                    user=random.choice(usuarios_legales)
                )
        
        self.stdout.write(
            self.style.SUCCESS('Datos de expedientes creados exitosamente')
        )
