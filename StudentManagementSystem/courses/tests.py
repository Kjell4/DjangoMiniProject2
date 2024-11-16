from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from courses.models import Course
from users.models import User
from django.utils.crypto import get_random_string

def create_user():
    email = f'{get_random_string(8)}@example.com'
    username = get_random_string(8)  # Generate a random username
    return User.objects.create_user(username=username, email=email, password='password')

class CourseCreateViewTest(APITestCase):
    def setUp(self):
        # Create teacher user
        self.teacher_user = create_user()
        self.teacher_user.is_teacher = True
        self.teacher_user.save()

    def test_create_course_as_teacher(self):
        self.client.login(username=self.teacher_user.username, password='password')

        url = reverse('course_create')  # Make sure the path is correct
        data = {'name': 'New Course', 'description': 'Course Description'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.first().name, 'New Course')

    def test_create_course_as_non_teacher(self):
        non_teacher_user = create_user()
        self.client.login(username=non_teacher_user.username, password='password')

        url = reverse('course_create')
        data = {'name': 'New Course', 'description': 'Course Description'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


   


