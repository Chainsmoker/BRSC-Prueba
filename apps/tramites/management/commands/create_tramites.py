from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.tramites.models import Tramite, SeguimientoTramite, GastoTramite
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea trámites de ejemplo con seguimientos y gastos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Eliminando trámites existentes...'))
        GastoTramite.objects.all().delete()
        SeguimientoTramite.objects.all().delete()
        Tramite.objects.all().delete()

        usuarios = list(User.objects.exclude(username='user8'))
        if not usuarios:
            self.stdout.write(self.style.ERROR('No hay usuarios disponibles'))
            return

        tipos_tramite = [
            'Licencia de Construcción',
            'Declaratoria de Fábrica',
            'Conformidad de Obra',
            'Permiso de Demolición',
            'Certificado de Parámetros',
            'Licencia de Funcionamiento',
            'Rectificación de Áreas',
            'Habilitación Urbana',
            'Anteproyecto en Consulta',
            'Subdivisión de Lote',
            'Independización',
            'Acumulación de Lotes',
            'Regularización de Edificación',
            'Cambio de Uso',
            'Ampliación de Licencia',
        ]

        destinatarios = [
            'Municipalidad Provincial del Callao',
            'Municipalidad Distrital de Bellavista',
            'Municipalidad Distrital de La Perla',
            'Municipalidad Distrital de Carmen de la Legua',
            'SUNARP - Zona Registral IX',
            'COFOPRI',
            'Ministerio de Vivienda',
            'SEDAPAL',
            'Luz del Sur',
        ]

        partes = [
            'Santa Clara Bienes Raíces SAC',
            'Consorcio Inmobiliario del Callao',
            'Inversiones Túpac Amaru',
            'Desarrollos Canta Callao',
            'Propietario Individual',
        ]

        responsables = [
            'Abg. Carlos Mendoza',
            'Abg. María Torres',
            'Abg. Juan Pérez',
            'Abg. Ana Rodríguez',
            'Abg. Luis García',
        ]

        estados = ['En proceso', 'Finalizado', 'Presentado']

        fecha_inicio = datetime.now().date() - timedelta(days=300)

        self.stdout.write(self.style.SUCCESS('Creando trámites...'))

        for i in range(20):
            fecha_tramite = fecha_inicio + timedelta(days=i * 15)
            tipo = random.choice(tipos_tramite)
            
            tramite = Tramite.objects.create(
                fecha=fecha_tramite,
                ult_revision=fecha_tramite + timedelta(days=random.randint(30, 90)),
                destinatario=random.choice(destinatarios),
                partes_intervinientes=random.choice(partes),
                sumilla=f'<p>Trámite de {tipo} para proyecto inmobiliario ubicado en el Callao. '
                        f'Se solicita la aprobación correspondiente según expediente técnico adjunto.</p>',
                tramite_tipo=tipo,
                pendiente=f'<p>Subsanar observaciones técnicas del área de obras.</p>' if random.choice([True, False]) else '',
                concluido=random.choice([True, False]),
                responsable2=random.choice(usuarios)
            )

            num_seguimientos = random.randint(2, 5)
            
            for j in range(num_seguimientos):
                fecha_seg = fecha_tramite + timedelta(days=(j + 1) * 20)
                fecha_alerta = fecha_seg + timedelta(days=random.randint(10, 30))
                
                seguimiento = SeguimientoTramite.objects.create(
                    caso=tramite,
                    fecha_seguimiento=fecha_seg,
                    seguimiento=f'<p>Seguimiento {j+1}: Se realizó la presentación de documentación '
                               f'{"complementaria" if j > 0 else "inicial"}. '
                               f'{"Observaciones levantadas." if j > 1 else "Pendiente de revisión."}</p>',
                    fecha_pendiente=fecha_seg + timedelta(days=15) if random.choice([True, False]) else None,
                    pendiente=f'<p>Presentar planos actualizados y memoria descriptiva.</p>' if random.choice([True, False]) else '',
                    responsable=random.choice(responsables),
                    estado=random.choice(estados),
                    inter=random.choice([True, False]),
                    editor=random.choice([u.username for u in usuarios]),
                    usuario=random.choice(usuarios),
                    fecha_alerta=fecha_alerta,
                )

                if random.choice([True, False, False]):
                    num_gastos = random.randint(1, 3)
                    
                    for k in range(num_gastos):
                        fecha_gasto = fecha_seg + timedelta(days=k * 5)
                        
                        tipo_gasto = random.choice([
                            ('Pago de derecho de trámite', 'Recibo Municipal'),
                            ('Tasación de predio', 'Informe de tasación'),
                            ('Honorarios profesionales', 'Recibo por honorarios'),
                            ('Copias certificadas', 'Comprobante de pago'),
                            ('Publicación en diario', 'Recibo de publicación'),
                            ('Gastos notariales', 'Minuta notarial'),
                        ])

                        usa_soles = random.choice([True, False])
                        
                        GastoTramite.objects.create(
                            seguimiento=seguimiento,
                            fecha=fecha_gasto,
                            detalle=tipo_gasto[0],
                            sustento=tipo_gasto[1],
                            codigo_pago=f'PAG-{random.randint(1000, 9999)}',
                            gastos_soles=random.uniform(200, 5000) if usa_soles else None,
                            gastos_dolares=random.uniform(50, 1500) if not usa_soles else None,
                            editor=random.choice([u.username for u in usuarios]),
                            usuario=random.choice(usuarios),
                        )

            self.stdout.write(
                self.style.SUCCESS(f'✓ Trámite {tramite.kardex} creado con {num_seguimientos} seguimientos')
            )

        total_tramites = Tramite.objects.count()
        total_seguimientos = SeguimientoTramite.objects.count()
        total_gastos = GastoTramite.objects.count()

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS(f'Trámites creados: {total_tramites}'))
        self.stdout.write(self.style.SUCCESS(f'Seguimientos creados: {total_seguimientos}'))
        self.stdout.write(self.style.SUCCESS(f'Gastos creados: {total_gastos}'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('✓ Comando ejecutado exitosamente'))
