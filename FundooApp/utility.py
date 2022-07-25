from functools import wraps
import jwt
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import request
from userlogin.models import User
from rest_framework_simplejwt.backends import TokenBackend
from fundoo.settings import SIMPLE_JWT


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs,):
        token = None
        print("HIIIII")
        if 'Token' in request.headers:
            token = request.headers.get('Token')
        if not token:
            return Response("Token Missing")
        try:
            data = jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=SIMPLE_JWT["ALGORITHM"])
            current_user = User.objects.filter(id=data['user_id']).first()
            print(current_user)
            user = {'user': current_user}
        except:
            return Response('Token is invalid')

        return f(*args, **user)

    return decorated


def decode_token():
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=True)
        user = valid_data['user']
        return Response(user)
    except ValidationError as v:
        print('validation error', v)
        return Response(str(v))

