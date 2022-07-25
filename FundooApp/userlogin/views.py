import logging

from rest_framework.views import APIView
import json
from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .tasks import test_func

logger = logging.getLogger(__name__)


class Register(APIView):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        phone_no = data.get('phone_no')
        password = data.get('password')
        user_data = {
            'firstname': firstname,
            'lastname': lastname,
            'phone_no': phone_no,
            'email': email,
            'password': password
        }
        all_users = User.objects.all()
        for user in all_users:
            if user.firstname.lower() == user_data.get('firstname').lower() and user.lastname.lower() == user_data.get('lastname').lower():
                logger.warning("User Name already exists")
                return Response({"message": "User name already exists", "status": 406})
            if user.email == user_data.get('email') and user.phone_no == user_data.get('phone_no'):
                logger.warning("User already exists")
                return Response({"message": "User already exists", "status": 406})

        user = User.objects.create(**user_data)

        logger.info("User Created")
        return Response({"message": "User Created", "status": 201})


class Login(APIView):

    def get(self, request):
        email = request.query_params.get("email")
        password = request.query_params.get("password")
        user = User.objects.filter(email=email).first()
        if user:
            if user.password == password:
                serializer = UserSerializer(user)
                auth_user = authenticate(email=email, password=password)
                print(auth_user)
                if auth_user is None:
                    return Response({"message": "Check your email/password", "status": 400})

                test_func.delay()

                refresh = RefreshToken.for_user(user)
                logger.info("User is Logged In")
                return Response({"message": "User is Logged In", "access": str(refresh.access_token),
                                 "refresh": str(refresh), "status": 200})
            logger.warning("Incorrect Password")
            return Response({"message": "Incorrect Password", "status": 404})
        return Response({"message": "No user Found", "status": 404})


class GetAllUsers(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        logger.info("All Users Displayed")
        return Response({"message": serializer.data, "status": 200})


class ActivateUser(APIView):

    def patch(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("User Account is Activated")
            return Response({'message': 'Account is activated now you can login', 'Code': 200})
        else:
            logger.warning("Error occurred while updating")
            return Response({"message": serializer.errors, "status": 404})


class AuthUserCheck(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self):
        return self.request.user