# students/serializers.py
from rest_framework import serializers
from attendance.serializers import AttendanceSerializer
from courses.serializers import CourseSerializer
from grades.serializers import GradeSerializer
from .models import Student
from courses.models import Course
from grades.models import Grade
from attendance.models import Attendance

class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    grades = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()
    

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'dob', 'registration_date', 'courses', 'grades', 'attendance')

    def get_courses(self, obj):
        courses = Course.objects.filter(enrollment__student=obj)
        return CourseSerializer(courses, many=True).data

    def get_grades(self, obj):
        grades = Grade.objects.filter(student=obj)
        return GradeSerializer(grades, many=True).data

    def get_attendance(self, obj):
        attendance = Attendance.objects.filter(student=obj)
        return AttendanceSerializer(attendance, many=True).data
