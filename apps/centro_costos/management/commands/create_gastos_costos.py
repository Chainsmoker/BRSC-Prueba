from django.core.management.base import BaseCommand
from apps.centro_costos.models import (
    CentroDeCostos, TipoDeGasto, Actividad, GastoTA2020,
    CantaCallao, NuevoGasto, Gasto, GastoN9
)
from apps.accounts.models import User
from faker import Faker
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Crea datos de prueba para centro de costos'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        centros = []
        for i in range(10):
            centro = CentroDeCostos.objects.create(
                nombre=fake.company()
            )
            centros.append(centro)
        
        tipos_gasto = []
        tipos_nombres = ['Servicios', 'Materiales', 'Personal', 'Transporte', 'Equipos', 'Suministros', 'Mantenimiento', 'Comunicaciones']
        for nombre in tipos_nombres:
            tipo = TipoDeGasto.objects.create(nombre=nombre)
            tipos_gasto.append(tipo)
        
        actividades = []
        for i in range(30):
            actividad = Actividad.objects.create(
                nombre=f"Actividad {fake.catch_phrase()}",
                codigo=f"ACT-{fake.unique.numerify(text='####')}",
                centro_de_costos=random.choice(centros),
                tipo=random.choice(['Por separado', 'A todo costo']),
                responsable=fake.name()
            )
            actividades.append(actividad)
        
        for i in range(100):
            GastoTA2020.objects.create(
                actividad=random.choice(actividades),
                item=f"Item-{i+1}",
                fecha=fake.date_between(start_date='-2y', end_date='today'),
                detalle=fake.text(max_nb_chars=200),
                documento=fake.bothify(text='DOC-####-????'),
                debe=Decimal(str(round(random.uniform(100, 10000), 2))),
                haber=Decimal(str(round(random.uniform(100, 10000), 2))),
                tipo_gasto=random.choice(tipos_gasto)
            )
        
        for i in range(50):
            CantaCallao.objects.create(
                codigo=f"CC-{fake.unique.numerify(text='######')}",
                fecha=fake.date_between(start_date='-1y', end_date='today'),
                concepto=fake.bs(),
                detalle=fake.text(max_nb_chars=100),
                referencia=fake.bothify(text='REF-????-####'),
                monto1=str(round(random.uniform(100, 5000), 2)),
                monto2=str(round(random.uniform(100, 5000), 2))
            )
        
        nuevos_gastos = []
        for i in range(5):
            nuevo = NuevoGasto.objects.create(
                nombre=f"Gasto {fake.word().capitalize()}",
                url=f"/gastos/{fake.slug()}",
                flag=random.choice([True, False])
            )
            nuevos_gastos.append(nuevo)
        
        for i in range(100):
            Gasto.objects.create(
                origen=random.choice(nuevos_gastos),
                codigo=f"G-{fake.unique.numerify(text='########')}",
                fecha=fake.date_between(start_date='-1y', end_date='today'),
                detalle=fake.text(max_nb_chars=200),
                referencia=fake.bothify(text='REF-????-####'),
                monto_soles=Decimal(str(round(random.uniform(50, 15000), 2))) if random.choice([True, False]) else None,
                monto_dolares=Decimal(str(round(random.uniform(10, 4000), 2))) if random.choice([True, False]) else None,
                actividad=random.choice(actividades).nombre,
                tipo_gasto=random.choice(tipos_gasto).nombre,
                es_ingreso=random.choice([True, False]),
                editor=fake.name()
            )
        
        users = User.objects.all()
        juzgados = ['Juzgado Civil', 'Juzgado Penal', 'Juzgado Laboral', 'Juzgado Familia', 'Juzgado Comercial']
        materias = ['Civil', 'Penal', 'Laboral', 'Familia', 'Comercial', 'Administrativo']
        
        for i in range(50):
            GastoN9.objects.create(
                expediente=f"EXP-{fake.numerify(text='#####-####')}",
                juzgado=random.choice(juzgados),
                demandante=fake.name(),
                demandado=fake.name(),
                materia=random.choice(materias),
                fecha=fake.date_between(start_date='-2y', end_date='today'),
                escrito=fake.text(max_nb_chars=300),
                concepto=fake.sentence(nb_words=6),
                monto_soles=Decimal(str(round(random.uniform(500, 20000), 2))) if random.choice([True, False]) else None,
                monto_dolares=Decimal(str(round(random.uniform(100, 5000), 2))) if random.choice([True, False]) else None
            )
        
        self.stdout.write(
            self.style.SUCCESS('Datos de centro de costos creados exitosamente')
        )
