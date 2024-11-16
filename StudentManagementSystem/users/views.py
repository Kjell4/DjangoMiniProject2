from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
import logging
from rest_framework import status
from .serializers import UserCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})

logger = logging.getLogger('django')

class UserRegistrationView(APIView):
    @swagger_auto_schema(
        operation_summary="User Registration",
        operation_description="Register a new user. Returns user details upon successful registration.",
        request_body=UserCreateSerializer,
        responses={201: UserCreateSerializer},
    )

    def post(self, request, *args, **kwargs):
        # Обрабатываем регистрацию
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f'New user registered: {user.email}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    