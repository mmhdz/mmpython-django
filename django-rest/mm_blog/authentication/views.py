from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView



class SingUpView(CreateAPIView):
    serializer_class = SingUpSerilizer
    permission_classes = (AllowAny,)



class SingInView(APIView):
    authentication_classes = [BasicAuthentication]

    def post(self, request): 
        return Response(status=status.HTTP_200_OK, data="Success")

   
    