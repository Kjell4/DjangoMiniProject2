# courses/views.py
from requests import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permissions import IsTeacher, IsAdmin
import django_filters
from django.core.cache import cache
import logging
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CourseCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a New Course",
        operation_description="Allows teachers to create a new course.",
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            403: openapi.Response(description="Forbidden - Only teachers can create courses"),
            400: openapi.Response(description="Bad Request - Validation errors"),
        },
    )

    def post(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated or not request.user.is_teacher:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseSerializer(data=request.data)
        
        if serializer.is_valid():
       
            course = serializer.save(teacher=request.user) 
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsTeacher()]  
        return [IsAuthenticated()] 
    
    def perform_update(self, serializer):
        course = serializer.save()
        
       
        cache.delete('courses_list')  

    @swagger_auto_schema(
        operation_summary="List Courses",
        operation_description="Retrieve a list of all available courses.",
        responses={200: CourseSerializer(many=True)},
    )

    def list(self, request, *args, **kwargs):
       
        cached_courses = cache.get('courses_list')

        if cached_courses:
            return Response(cached_courses) 

      
        courses = Course.objects.all()  
        serialized_courses = CourseSerializer(courses, many=True).data

        
        cache.set('courses_list', serialized_courses, timeout=60*15)
        
        return Response(serialized_courses)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        student = self.request.user.student_profile 
        course = serializer.validated_data['course']
        serializer.save(student=student)

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()] 
        return [IsAuthenticated()]

class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    instructor = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name', 'instructor']

logger = logging.getLogger('django')

class EnrollStudentView(APIView):
    @swagger_auto_schema(
        operation_summary="Enroll Student in a Course",
        operation_description="Allows a student to enroll in a specific course by ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Course ID"),
            },
            required=['course_id'],
        ),
        responses={201: openapi.Response(description="Successfully enrolled")},
    )
    
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = Course.objects.get(id=course_id)
        student = request.user  

        enrollment = Enrollment.objects.create(course=course, student=student)
        logger.info(f'{student.email} enrolled in course: {course.name}')
        return Response({"message": "Successfully enrolled"}, status=201)

def get_courses():
    cached_courses = cache.get('courses_list')
    if cached_courses:
        logger.info('Cache hit for courses list')
    else:
        logger.info('Cache miss for courses list')
        courses = Course.objects.all()
        cache.set('courses_list', courses, timeout=60*15) 
    return cached_courses or courses
