# attendance/views.py
from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsTeacher()]  # Преподаватели могут редактировать посещаемость
        return [IsAuthenticated(), IsAdmin()]  # Администраторы имеют полный доступ

logger = logging.getLogger('django')

class MarkAttendanceView(APIView):
    @swagger_auto_schema(
        operation_summary="Mark Attendance",
        operation_description="Students can mark their attendance for a course.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Course ID"),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description="Attendance status ('present' or 'absent')"),
            },
            required=['course_id', 'status'],
        ),
        responses={200: openapi.Response(description="Attendance marked successfully")},
    )

    def post(self, request, *args, **kwargs):
        student = request.user  # Авторизованный студент
        course_id = request.data.get('course_id')
        status = request.data.get('status')

        # Создаем или обновляем запись о посещаемости
        attendance, created = Attendance.objects.update_or_create(
            student=student, course_id=course_id,
            defaults={'status': status}
        )
        action = 'Created' if created else 'Updated'
        logger.info(f'{action} attendance for {student.email} in course {course_id} with status {status}')
        return Response({"message": "Attendance marked successfully"}, status=200)
