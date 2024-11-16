# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Student

@shared_task
def send_attendance_reminder():
    # Логика отправки напоминания студентам
    students = Student.objects.all()
    for student in students:
        send_mail(
            'Напоминание: отметьте посещаемость',
            'Пожалуйста, не забудьте отметить вашу посещаемость сегодня.',
            'from@example.com',
            [student.email],
            fail_silently=False,
        )

# notifications/tasks.py
@shared_task
def send_grade_update_notification(student_id, course_id, new_grade):
    student = Student.objects.get(id=student_id)
    send_mail(
        'Обновление оценки',
        f'Ваша новая оценка по курсу {course_id} - {new_grade}.',
        'from@example.com',
        [student.email],
        fail_silently=False,
    )

# notifications/tasks.py
@shared_task
def send_daily_report():
    # Логика для сбора данных и отправки отчетов
    # Например, по посещаемости и оценкам
    print("Ежедневный отчет отправлен!")
