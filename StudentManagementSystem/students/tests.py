from django.contrib.auth import get_user_model
from students.models import Student
from django.test import TestCase

class StudentModelTest(TestCase):

    def test_create_student(self):

        User = get_user_model()
        
        user = User.objects.create_user(
            username="testuser", 
            password="password123", 
            email="testuser@example.com"
        )
        

        student = Student.objects.create(
            user=user, 
            name="John Doe", 
            email="john@example.com", 
            dob="2000-01-01"
        )
        
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(student.email, "john@example.com")
        self.assertEqual(student.dob, "2000-01-01")

    def test_student_str(self):

        User = get_user_model()
        
        user = User.objects.create_user(
            username="testuser", 
            password="password123", 
            email="testuser2@example.com"
        )
  
        student = Student.objects.create(
            user=user, 
            name="Jane Doe", 
            email="jane@example.com", 
            dob="1998-05-15"
        )
        
        self.assertEqual(str(student), "Jane Doe")



