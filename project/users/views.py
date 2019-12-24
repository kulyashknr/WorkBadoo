from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.serializers import CompanySerializer, WorkerSerializer, UserFullSerializer


class IsCompany(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class Register(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = UserFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterCompany(APIView):
    http_method_names = ['post']
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterWorker(APIView):
    http_method_names = ['post']
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
