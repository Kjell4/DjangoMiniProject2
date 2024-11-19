from unittest.mock import patch
from django.core.cache import cache
from notifications.tasks import send_attendance_reminder
from django.test import TestCase
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from notifications.tasks import send_daily_report

class CeleryTaskTestCase(TestCase):
    @patch('notifications.tasks.send_mail')
    def test_send_attendance_reminder(self, mock_send_mail):
     
        send_attendance_reminder()
        
        mock_send_mail.assert_called_with(
            'Reminder: Mark Your Attendance',
            'Please remember to mark your attendance today.',
            'from@example.com',
            ['student@example.com'],
            fail_silently=False,
        )

class CeleryBeatTestCase(TestCase):
    def test_periodic_task_scheduled(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1, period=IntervalSchedule.DAYS
        )
        task = PeriodicTask.objects.create(
            interval=schedule,
            name="Send daily report",
            task='notifications.tasks.send_daily_report',
        )
        self.assertTrue(task)
