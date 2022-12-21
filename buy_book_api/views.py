from buy_book_api.serializer import *
from book.models import Buybook,Book
from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
from book.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginViewSet(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ShowBooks(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class BuyBookViewset(viewsets.ModelViewSet):
    queryset = Buybook.objects.all()
    serializer_class = BuyBookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class UserProfileViewset(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class=UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

class UserProfileUpdateViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class=UserProfileSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminRegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class=BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class BuyBookUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Buybook.objects.all()
    serializer_class=BuybookUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class AdminProfileViewSet(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class=AdminProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class BuyBookViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ShowBuyBookSerializer

    def get_queryset(self):
        return Buybook.objects.filter(username=self.request.user.username)

class ReturnBookViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,id):
        if Buybook.objects.filter(id=id).exists():
            buybook=Buybook.objects.get(id=id)
            book=Book.objects.get(id=buybook.bookdetail.id)
            book.bookquantity=int(book.bookquantity)+int(buybook.buybookquantity)
            book.deleted=False
            book.save()
            buybook.delete()
            return JsonResponse({'Return-book-info':'Your book will be Return successfully'})
        else:
            return JsonResponse({'error-info':'User not found'})

class AllRegisterUser(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class=UserRegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class AdminRegisterViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = AdminRegisterSerializer

    def get_queryset(self):
        return User.objects.filter(is_superuser=True)

class UserRegisterViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)






