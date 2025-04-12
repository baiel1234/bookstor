from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import RegisterSerializer, LoginSerializer, BookSerializer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserUpdateSerializer, OwnerSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Регистрация успешна"})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Вход выполнен", "user_id": user.id})
        return Response(serializer.errors, status=400)

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookSearchView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        books = Book.objects.filter(title__icontains=query)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def perform_update(self, serializer):
        # Обновлять может только владелец
        if self.request.user != self.get_object().owner:
            raise PermissionDenied("Вы не являетесь владельцем этой книги.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionDenied("Вы не являетесь владельцем этой книги.")
        instance.delete()

class BookCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = OwnerSerializer(request.user)
        return Response(serializer.data)

    def delete(self, request):
        request.user.delete()
        return Response({"detail": "Пользователь удалён"}, status=status.HTTP_204_NO_CONTENT)