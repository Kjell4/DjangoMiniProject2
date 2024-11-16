# grades/models.py
from django.db import models
from students.models import Student
from courses.models import Course
from users.models import User  # Преподаватель (User)

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)  # Например, A, B, C, etc.
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grades")

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.grade}"
