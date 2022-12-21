from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from book.models import Buybook, Book, User

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from django.http import JsonResponse




class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["username"]=self.user.username
        data["is_student"]=self.user.is_student
        data["email"]=self.user.email
        data["phone"] = self.user.phone
        data["firstname"]=self.user.first_name
        data["lastname"]=self.user.last_name


        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password','phone','is_student']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data["password"] = make_password(password)
        instance = super().create(validated_data)
        instance.save()
        return instance


class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password', 'is_superuser','phone','is_student']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data["password"] = make_password(password)
        instance = super().create(validated_data)
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'bookname', 'bookquantity', 'booklanguage', 'bookprice', 'bookpage', 'authername', 'deleted']


class BuyBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buybook
        fields = ['id', 'bookdetail', 'username', 'buydate', 'returndate', 'buybookquantity', 'phone', 'buy', 'deleted']

    def validate(self, data):
        book = data['bookdetail']
        buybookquantity = data['buybookquantity']
        if book.bookquantity < buybookquantity:
            raise serializers.ValidationError(f'book must be {book.bookquantity}')
        return data

    def create(self, validated_data):
        book = validated_data['bookdetail']
        buybookquantity = validated_data['buybookquantity']
        total = int(book.bookquantity) - int(buybookquantity)
        if total == 0:
            book.deleted = True
        else:
            book.deleted = False
        book.bookquantity = total
        book.save()
        instance = super().create(validated_data)

        return instance


class showBookserializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bookname', 'booklanguage', 'bookprice', 'bookpage', 'authername']


class ShowBuyBookSerializer(serializers.ModelSerializer):
    bookdetail = showBookserializer(read_only=True)

    class Meta:
        model = Buybook
        fields = ['id', 'bookdetail', 'username', 'buydate', 'returndate', 'buybookquantity', 'phone']


class BuybookUserSerializer(serializers.ModelSerializer):
    bookdetail = serializers.StringRelatedField(read_only=True)

    booklanguage = serializers.SerializerMethodField("get_booklanguage")
    bookprice = serializers.SerializerMethodField("get_bookprice")
    authername = serializers.SerializerMethodField("get_authername")

    def get_authername(self, obj):
        return obj.bookdetail.authername

    def get_booklanguage(self, obj):
        return obj.bookdetail.booklanguage

    def get_bookprice(self, obj):
        return obj.bookdetail.bookprice

    class Meta:
        model = Buybook
        fields = ['id', 'bookdetail', 'booklanguage', 'bookprice', 'authername', 'username', 'phone']


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_superuser','phone','is_student']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', 'first_name',
                  'last_name', 'email','phone','is_student']
