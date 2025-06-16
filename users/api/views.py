from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserDataSerializer, UserUpdateSerializer
from users.models import User

class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer
    
    def get(self, request):
        serializer = UserDataSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request):
        user = User.objects.get(id = request.user.id) 
        serializer = self.serializer_class(user, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
