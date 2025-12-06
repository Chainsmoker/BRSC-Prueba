from django.core.management.base import BaseCommand
from apps.partidas_planos.models import Partida, Plano
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Crea partidas y planos de prueba'

    def handle(self, *args, **kwargs):
        Partida.objects.all().delete()
        Plano.objects.all().delete()

        partidas_data = [
            {
                'codigo': 'P-001',
                'partida': 'Trabajos Preliminares',
                'descripcion': 'Limpieza y preparación del terreno',
                'pg': 'PG-2024-001',
                'ubicacion': 'Lote A - Mz. 1',
                'costo': '15000.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. Carlos Mendoza'
            },
            {
                'codigo': 'P-002',
                'partida': 'Movimiento de Tierras',
                'descripcion': 'Excavación para cimentación',
                'pg': 'PG-2024-002',
                'ubicacion': 'Lote A - Mz. 1',
                'costo': '25000.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. María Torres'
            },
            {
                'codigo': 'P-003',
                'partida': 'Obras de Concreto Simple',
                'descripcion': 'Solados y falso piso',
                'pg': 'PG-2024-003',
                'ubicacion': 'Lote B - Mz. 2',
                'costo': '18500.00',
                'centro_costos': 'Canta Callao',
                'responsable': 'Ing. Juan Pérez'
            },
            {
                'codigo': 'P-004',
                'partida': 'Obras de Concreto Armado',
                'descripcion': 'Columnas y vigas principales',
                'pg': 'PG-2024-004',
                'ubicacion': 'Lote B - Mz. 2',
                'costo': '45000.00',
                'centro_costos': 'Canta Callao',
                'responsable': 'Ing. Ana Gómez'
            },
            {
                'codigo': 'P-005',
                'partida': 'Muros y Tabiques',
                'descripcion': 'Albañilería de ladrillo',
                'pg': 'PG-2024-005',
                'ubicacion': 'Lote C - Mz. 3',
                'costo': '22000.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. Roberto Silva'
            },
            {
                'codigo': 'P-006',
                'partida': 'Revoques y Enlucidos',
                'descripcion': 'Tarrajeo de muros interiores',
                'pg': 'PG-2024-006',
                'ubicacion': 'Lote C - Mz. 3',
                'costo': '16000.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. Patricia Rojas'
            },
            {
                'codigo': 'P-007',
                'partida': 'Pisos y Pavimentos',
                'descripcion': 'Instalación de cerámico',
                'pg': 'PG-2024-007',
                'ubicacion': 'Lote D - Mz. 4',
                'costo': '28000.00',
                'centro_costos': 'Canta Callao',
                'responsable': 'Ing. Luis Ramírez'
            },
            {
                'codigo': 'P-008',
                'partida': 'Zócalos y Contrapisos',
                'descripcion': 'Zócalo de porcelanato',
                'pg': 'PG-2024-008',
                'ubicacion': 'Lote D - Mz. 4',
                'costo': '12000.00',
                'centro_costos': 'Canta Callao',
                'responsable': 'Ing. Carmen Vega'
            },
            {
                'codigo': 'P-009',
                'partida': 'Carpintería de Madera',
                'descripcion': 'Puertas y marcos',
                'pg': 'PG-2024-009',
                'ubicacion': 'Lote E - Mz. 5',
                'costo': '19500.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. Diego Castro'
            },
            {
                'codigo': 'P-010',
                'partida': 'Instalaciones Sanitarias',
                'descripcion': 'Red de agua y desagüe',
                'pg': 'PG-2024-010',
                'ubicacion': 'Lote E - Mz. 5',
                'costo': '32000.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. Sofía Morales'
            },
            {
                'codigo': 'P-011',
                'partida': 'Instalaciones Eléctricas',
                'descripcion': 'Cableado y puntos eléctricos',
                'pg': 'PG-2024-011',
                'ubicacion': 'Lote F - Mz. 6',
                'costo': '27000.00',
                'centro_costos': 'Canta Callao',
                'responsable': 'Ing. Fernando Ortiz'
            },
            {
                'codigo': 'P-012',
                'partida': 'Pintura',
                'descripcion': 'Pintura látex en muros',
                'pg': 'PG-2024-012',
                'ubicacion': 'Lote F - Mz. 6',
                'costo': '14000.00',
                'centro_costos': 'Canta Callao',
                'responsable': 'Ing. Gabriela Núñez'
            },
            {
                'codigo': 'P-013',
                'partida': 'Aparatos Sanitarios',
                'descripcion': 'Instalación de sanitarios',
                'pg': 'PG-2024-013',
                'ubicacion': 'Lote G - Mz. 7',
                'costo': '11500.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. Ricardo Flores'
            },
            {
                'codigo': 'P-014',
                'partida': 'Vidrios y Cristales',
                'descripcion': 'Ventanas de aluminio',
                'pg': 'PG-2024-014',
                'ubicacion': 'Lote G - Mz. 7',
                'costo': '24000.00',
                'centro_costos': 'Tupac Amaru',
                'responsable': 'Ing. Valeria Soto'
            },
            {
                'codigo': 'P-015',
                'partida': 'Cerrajería',
                'descripcion': 'Chapas y bisagras',
                'pg': 'PG-2024-015',
                'ubicacion': 'Lote H - Mz. 8',
                'costo': '8500.00',
                'centro_costos': 'Canta Callao',
                'responsable': 'Ing. Héctor Paredes'
            }
        ]

        planos_data = [
            {
                'partida': 'Arquitectura General',
                'descripcion': 'Plano de distribución general',
                'pg': 'PG-2024-ARQ-001',
                'ubicacion': 'Proyecto Completo',
                'costo': '5000.00',
                'centro_costos': 'Tupac Amaru'
            },
            {
                'partida': 'Estructuras - Cimentación',
                'descripcion': 'Plano de zapatas y cimientos',
                'pg': 'PG-2024-EST-001',
                'ubicacion': 'Todos los lotes',
                'costo': '6500.00',
                'centro_costos': 'Tupac Amaru'
            },
            {
                'partida': 'Instalaciones Eléctricas',
                'descripcion': 'Plano de circuitos eléctricos',
                'pg': 'PG-2024-ELE-001',
                'ubicacion': 'Manzana 1-4',
                'costo': '4500.00',
                'centro_costos': 'Canta Callao'
            },
            {
                'partida': 'Instalaciones Sanitarias',
                'descripcion': 'Plano de redes de agua',
                'pg': 'PG-2024-SAN-001',
                'ubicacion': 'Manzana 1-4',
                'costo': '5500.00',
                'centro_costos': 'Canta Callao'
            },
            {
                'partida': 'Arquitectura - Fachadas',
                'descripcion': 'Plano de elevaciones',
                'pg': 'PG-2024-ARQ-002',
                'ubicacion': 'Lotes frontales',
                'costo': '4000.00',
                'centro_costos': 'Tupac Amaru'
            },
            {
                'partida': 'Estructuras - Columnas',
                'descripcion': 'Plano de detalle de columnas',
                'pg': 'PG-2024-EST-002',
                'ubicacion': 'Todos los lotes',
                'costo': '5800.00',
                'centro_costos': 'Tupac Amaru'
            },
            {
                'partida': 'Arquitectura - Cortes',
                'descripcion': 'Plano de cortes transversales',
                'pg': 'PG-2024-ARQ-003',
                'ubicacion': 'Proyecto Completo',
                'costo': '3800.00',
                'centro_costos': 'Canta Callao'
            },
            {
                'partida': 'Instalaciones - Gas',
                'descripcion': 'Plano de red de gas',
                'pg': 'PG-2024-GAS-001',
                'ubicacion': 'Manzana 5-8',
                'costo': '3500.00',
                'centro_costos': 'Canta Callao'
            },
            {
                'partida': 'Paisajismo',
                'descripcion': 'Plano de áreas verdes',
                'pg': 'PG-2024-PAI-001',
                'ubicacion': 'Áreas comunes',
                'costo': '4200.00',
                'centro_costos': 'Tupac Amaru'
            },
            {
                'partida': 'Señalización',
                'descripcion': 'Plano de señalética',
                'pg': 'PG-2024-SEÑ-001',
                'ubicacion': 'Todo el complejo',
                'costo': '2800.00',
                'centro_costos': 'Tupac Amaru'
            },
            {
                'partida': 'Estructuras - Vigas',
                'descripcion': 'Plano de detalle de vigas',
                'pg': 'PG-2024-EST-003',
                'ubicacion': 'Todos los lotes',
                'costo': '6000.00',
                'centro_costos': 'Canta Callao'
            },
            {
                'partida': 'Evacuación',
                'descripcion': 'Plano de evacuación y seguridad',
                'pg': 'PG-2024-EVA-001',
                'ubicacion': 'Todo el complejo',
                'costo': '3200.00',
                'centro_costos': 'Canta Callao'
            }
        ]

        fecha_base = datetime.now() - timedelta(days=180)
        
        self.stdout.write('Creando partidas...')
        for i, data in enumerate(partidas_data):
            fecha = fecha_base + timedelta(days=i * 12)
            Partida.objects.create(
                codigo=data['codigo'],
                partida=data['partida'],
                fecha=fecha,
                descripcion=data['descripcion'],
                pg=data['pg'],
                ubicacion=data['ubicacion'],
                costo=data['costo'],
                centro_costos=data['centro_costos'],
                responsable=data['responsable']
            )
            self.stdout.write(f'  ✓ Partida {data["codigo"]} creada')

        self.stdout.write('\nCreando planos...')
        for i, data in enumerate(planos_data):
            fecha = fecha_base + timedelta(days=i * 15)
            Plano.objects.create(
                partida=data['partida'],
                fecha=fecha,
                descripcion=data['descripcion'],
                pg=data['pg'],
                ubicacion=data['ubicacion'],
                costo=data['costo'],
                centro_costos=data['centro_costos']
            )
            self.stdout.write(f'  ✓ Plano {data["partida"]} creado')

        total_partidas = Partida.objects.count()
        total_planos = Plano.objects.count()

        self.stdout.write(self.style.SUCCESS(f'\n✓ Se crearon {total_partidas} partidas y {total_planos} planos exitosamente'))
