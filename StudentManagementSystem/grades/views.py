# grades/views.py
from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsTeacher()]  # Преподаватели могут редактировать оценки
        return [IsAuthenticated(), IsAdmin()]  # Администраторы могут редактировать любые записи
    
logger = logging.getLogger('django')

class UpdateGradeView(APIView):
    @swagger_auto_schema(
        operation_summary="Update Student Grade",
        operation_description="Allows a teacher to update or create a grade for a student in a specific course.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'student': openapi.Schema(type=openapi.TYPE_INTEGER, description="Student ID"),
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Course ID"),
                'grade': openapi.Schema(type=openapi.TYPE_STRING, description="Grade (e.g., A, B, C)"),
            },
            required=['student', 'course_id', 'grade'],
        ),
        responses={200: openapi.Response(description="Grade updated successfully")},
    )

    def post(self, request, *args, **kwargs):
        student = request.data.get('student')
        course_id = request.data.get('course_id')
        grade = request.data.get('grade')
        
        # Обновление или создание записи о оценке
        grade_record, created = Grade.objects.update_or_create(
            student_id=student, course_id=course_id,
            defaults={'grade': grade}
        )
        action = 'Created' if created else 'Updated'
        logger.info(f'{action} grade for student {student} in course {course_id} with grade {grade}')
        return Response({"message": "Grade updated successfully"}, status=200)

