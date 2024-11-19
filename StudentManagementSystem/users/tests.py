from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class RoleBasedPermissionsTestCase(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            username="admin", email="admin@example.com", password="adminpass", role="admin"
        )
        self.teacher = get_user_model().objects.create_user(
            username="teacher", email="teacher@example.com", password="teacherpass", role="teacher"
        )
        self.student = get_user_model().objects.create_user(
            username="student", email="student@example.com", password="studentpass", role="student"
        )

    def test_admin_access(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_access(self):
        self.client.login(username="teacher", password="teacherpass")
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_access(self):
        self.client.login(username="student", password="studentpass")
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  
