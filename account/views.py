import bcrypt
import hashlib
import json
import jwt
import os
import requests
import sys

from django.http                    import JsonResponse, HttpResponse
from django.core.validators         import validate_email, RegexValidator
from django.core.exceptions         import ValidationError
from django.shortcuts               import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http              import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail               import EmailMessage
from django.utils.encoding          import force_bytes, force_text
from django.views                   import View

from my_settings                    import  SECRET_KEY, EMAIL, ALGORITHM

from .text                          import message
from account.utils                  import login_decorator
from .tokens                        import account_activation_token
from .models                        import User

class SignUpView(View):
    def post(self, request):
        data                = json.loads(request.body)
        try:
            validate_email(data['email'])

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({'message':'EXISTS_EMAIL'}, status = 400)

            user = User.objects.create(
                email       = data["email"],
                password    = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()),
                is_active   = False
            )

            current_site = get_current_site(request)
            domain       = current_site.domain
            uid64        = urlsafe_base64_encode(force_bytes(user.pk))
            token        = account_activation_token.make_token(user)
            message_data = message(domain, uid64, token)

            mail_title  = "이메일 인증을 완료해주세요."
            mail_to     = data["email"]
            email       = EmailMessage(mail_title, message_data, to = [mail_to])
            email.send()
            
            return JsonResponse({"message":"SUCCESS"},status = 200)
        except ValidationError:
            return JsonResponse({"message" : "INVALID_EMAIL_OR_PASSWORD"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status = 400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status = 400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status = 400)

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

class Activate(View):
    def get(self,request, uid64, token):
        try:
            uid  = force_text(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                return redirect(EMAIL['REDIRECT_PAGE'])
            
            return JsonResponse({"message":"ALREADY_AUTH_COMPLETED"}, status=400)

        except ValidationError:
            return JsonResponse({"message":"TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"}, status=400)