from django.contrib import admin
from django.urls import path,include
from buy_book_api import views
from rest_framework.routers import DefaultRouter
from buy_book_api import views as vw
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

router = DefaultRouter()
router.register('api-user-register', vw.UserViewSet, basename='api-user-register')
router.register('api-admin-register', vw.AdminViewSet, basename='api-admin-register')
router.register('api-book', vw.BookViewSet, basename='api-book')
router.register('api-buy-book-user', vw.BuyBookUserViewSet, basename='api-buy-book-user')
router.register('api-show-book', vw.ShowBooks, basename='api-show-book')
router.register('api-show-buy-book', vw.BuyBookViewSet, basename='api-show-buy-book')
router.register('api-user-profile', vw.UserProfileViewset, basename='api-user-profile')
router.register('api-user-profile-update-delete', vw.UserProfileUpdateViewSet, basename='api-user-profile-update-delete')
router.register('api-buy-book', vw.BuyBookViewset, basename='api-buy-book')
router.register('api-all-user', vw.AllRegisterUser, basename='api-all-user')
router.register('api-register-admin-list', vw.AdminRegisterViewSet, basename='api-register-admin-list')
router.register('api-user-admin-list', vw.UserRegisterViewSet, basename='api-user-admin-list')
urlpatterns = [
    path('', include(router.urls)),
    path('api-login/', vw.LoginViewSet.as_view(), name='api-login'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-admin-profile/<int:pk>/', vw.AdminProfileViewSet.as_view(), name='api-admin-profile'),
    # path('api-admin-profile/<int:pk>/', vw.Adminprofileapi.as_view(), name='api-admin-profile'),
    path('api-return-book/<int:id>/', vw.ReturnBookViewSet.as_view(), name='api-return-book'),

]