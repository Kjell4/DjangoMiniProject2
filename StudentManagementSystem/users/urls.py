# users/urls.py
from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),  # Включаем все необходимые маршруты djoser для аутентификации
    path('auth/token/', include('djoser.urls.authtoken')),  # Для получения токенов аутентификации
]
