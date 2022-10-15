from django.shortcuts import render
import json
import bcrypt
import jwt
import re

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import views as auth_views

from .models import Users
from my_settings import SECRET_KEY, ALGORITHM

# Create your views here.


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            username = data['username']
            department = data['department']
            # 아이디가 존재하는지 확인
            if Users.objects.filter(username=username).exists():
                return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)
            # 비밀번호 암호화
            password = data['password'].encode('utf-8')  # 입력된 비밀번호를 인코딩
            password_crypt = bcrypt.hashpw(
                password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
            password_crypt = password_crypt.decode(
                'utf-8')  # 디비에 저장할 수 있는 형태로 디코딩
            # 아이디와 비밀번호 db에 저장
            Users.objects.create(
                username=username, password=password_crypt, department=department)
            return JsonResponse({'message': 'SUCCESS!'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Users.objects.filter(username=data['username']).exists():
                user = Users.objects.get(username=data['username'])
            #---------비밀번호 확인--------#
            # 사용자가 입력한 비밀번호를 인코딩하고, 사용자의 이메일과 매칭되는 DB의 비밀번호를 찾아와서 인코딩.
            # 이 두 값을 bcrypt.checkpw로 비교
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                # 토큰 발행
                token = jwt.encode(
                    {'username': data['username']}, SECRET_KEY, algorithm="HS256")
                # token = token.decode('utf-8') #이미 디코드된 것을 다시 디코드할 필요가 없는거 같은데 애매함
                return JsonResponse({'message': '로그인 성공', 'token': token}, status=200)

            else:
                return JsonResponse({'message': '비밀번호가 틀렸어요'}, status=200)

            return JsonResponse({'message': '등록되지 않은 이메일 입니다.'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class TokenCheckView(View):
    def post(self, request):
        data = json.loads(request.body)

        user_token_info = jwt.decode(
            data['token'], SECRET_KEY, algorithm='HS256')

        if Users.objects.filter(username=user_token_info['ussername']).exists():
            return HttpResponse(status=200)

        return HttpResponse(status=403)
