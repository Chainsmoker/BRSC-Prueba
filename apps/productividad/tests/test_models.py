from django.test import TestCase
from django.contrib.auth import get_user_model
from productividad.models import DailyActivity

User = get_user_model()

class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', email='u1@example.com', password='pass')

    def test_create_activity(self):
        a = DailyActivity.objects.create(user=self.user, date='2025-01-01', title='Tarea X')
        self.assertEqual(a.title, 'Tarea X')
