from rest_framework.exceptions import ValidationError
from .serializers import *
from rest_framework import generics, permissions,viewsets,views,status
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.parsers import MultiPartParser, FormParser

class RegisterAPI(generics.GenericAPIView):
    serializer_class = registerSerializer

    def post(self,request, *args, **kwargs):

        registerData = {
            "username":request.data["username"],
            "email":request.data["email"],
            "password":request.data["password"],
            "password2":request.data["password2"]
        }

        if registerData['password'] != registerData["password2"]:
            return Response({'message':"password not same"},status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=registerData)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()

        return Response({
            "user": userSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        },status=status.HTTP_201_CREATED)

#login api
class LoginAPI(generics.GenericAPIView):
    serializer_class = loginSerilaizer

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "user": userSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            },status=status.HTTP_200_OK)
    

# get user api
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = userSerializer

    def get_object(self):
        return self.request.user
