from django.core.management.base import BaseCommand
import csv
from django.utils import timezone
from django.contrib.auth import get_user_model
from productividad.models import DailyActivity


class Command(BaseCommand):
    help = 'Exporta reporte de actividades por usuario'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)
        parser.add_argument('--out', type=str, default='report.csv')


    def handle(self, *args, **options):
        uid = options['user_id']
        outfile = options['out']
        user = get_user_model().objects.get(id=uid)
        qs = DailyActivity.objects.filter(user=user).order_by('date')


        with open(outfile, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'title', 'description', 'score', 'scored_by', 'scored_at'])
            for a in qs:
                writer.writerow([a.date, a.title, a.description, a.score, getattr(a.scored_by, 'username', ''), a.scored_at])
        self.stdout.write(self.style.SUCCESS(f'Exportado {qs.count()} registros a {outfile}'))