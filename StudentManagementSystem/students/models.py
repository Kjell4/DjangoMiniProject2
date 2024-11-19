from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dob = models.DateField(verbose_name="Date of Birth")
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
