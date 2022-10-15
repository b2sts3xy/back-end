from django.shortcuts import render
import json
import bcrypt
import jwt
import re

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login

from .models import Users
from my_settings import SECRET_KEY, ALGORITHM

# Create your views here.


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']
            password = data['password']
            department = data['department']

            if Users.objects.filter(username=username).exists():
                return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)

            Users.objects.create(
                username=username, password=password, department=department)
            return JsonResponse({'message': 'SUCCESS!'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            Users.objects.get(
                password=request.data['password'], username=request.data['username'])
            return JsonResponse({'message': 'SUCCESS!'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
