# students/views.py
from requests import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsStudent, IsAdmin
import django_filters
from django.core.cache import cache

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsStudent()] 
        return [IsAuthenticated(), IsAdmin()]
    
    def perform_update(self, serializer):
        student = serializer.save()
        cache.delete(f'student_profile_{student.id}')

    def retrieve(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        
        cached_student = cache.get(f'student_profile_{student_id}')

        if cached_student:
            return Response(cached_student) 

        student = self.get_object()
        serialized_student = StudentSerializer(student).data

        cache.set(f'student_profile_{student_id}', serialized_student, timeout=60*15)
        
        return Response(serialized_student)

class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['name']