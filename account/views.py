import bcrypt
import hashlib
import json
import jwt
import os
import requests
import sys

from django.http            import JsonResponse
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from django.views           import View

from my_settings import SECRET_KEY, ALGORITHM

from account.utils  import login_decorator

from .models import User

class SignUpView(View):
    def post(self, request):
        data                = json.loads(request.body)
        password_validator  = RegexValidator(regex =  "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")             
        try:
            validate_email(data['email'])
            if not User.objects.filter(email = data['email']).exists():
                password_validator(data['password'])
                password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
                User(
                    email       = data['email'],
                    password    = password
                ).save()
                user    = User.objects.get(email=data['email'])
                token   = jwt.encode({"user_id":user.id}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')

                return JsonResponse({'token' : token}, status=200)
            return JsonResponse({'message': 'EXISTING_EMAIL'},status=401)
        
        except ValidationError:
            return JsonResponse({"message" : "INVALID_EMAIL_OR_PASSWORD"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status = 400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data['email'])
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user':user.id},SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
                    return JsonResponse({'token':token},status=200)
                return JsonResponse({'message':'WRONG_EMAIL_PASSWORD'},status=400)
            return JsonResponse({'message':'WRONG_EMAIL_PASSWORD'},status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'},status=400)
        except ValidationError:
            return JsonResponse({'message':'INVALID_EMAIL'},status=400)