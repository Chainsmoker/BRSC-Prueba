from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class DailyActivity(models.Model):
    SCORE_CHOICES = (
        (1, 'Bajo'),
        (2, 'Medio'),
        (3, 'Alto'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, null=True, blank=True)
    scored_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='scored_activities')
    scored_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date', 'title')
        ordering = ['-date', '-created_at']


    def score_activity(self, scorer, score_value):
        self.score = score_value
        self.scored_by = scorer
        self.scored_at = timezone.now()
        self.save()


    def __str__(self):
        return f"{self.user} - {self.date} - {self.title}"