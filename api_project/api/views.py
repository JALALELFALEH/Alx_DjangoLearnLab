from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .serializers import BookSerializer
from .models import Book

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' :
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]