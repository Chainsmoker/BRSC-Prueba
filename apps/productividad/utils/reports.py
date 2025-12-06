from django.db.models import Avg, Count
from .models import DailyActivity

def summary_for_user(user):
    qs = DailyActivity.objects.filter(user=user)
    return qs.values('date__year', 'date__month').annotate(avg_score=Avg('score'), activities=Count('id')).order_by('-date__year', '-date__month')