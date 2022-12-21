"""buybook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from book import views
from book import user_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Admin-dash/',views.AdminBaseView.as_view(),name='base'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('userregister/', views.UserRegisterView.as_view(), name='userregister'),
    path('user-register/', views.AllUserRegisterView.as_view(), name='user-register'),

    path('forgotpassword/', views.Forgotpasswordview.as_view(), name='forgotpassword'),
    path('add-book/', views.AddBookView.as_view(), name='addbook'),

    path('register-user-table/', views.RegisterUserTableView.as_view(), name='registerusertable'),
    path('register-admin-table/', views.RegisterAdminTableView.as_view(), name='registeradmintable'),
    path('show-book-table/', views.ShowBookTableView.as_view(), name='showbooktable'),

    path('buy-book-user-table/', views.BuyBookUserTableView.as_view(), name='buybookusertable'),
    path('edit-book/<int:id>/', views.EditBookView.as_view(), name='editbook'),
    path('delete-book/<int:id>/', views.DeleteBookView.as_view(), name='deletebook'),
    path('delete-user/<int:id>/', views.DeleteUserView.as_view(), name='deleteuser'),
    path('delete-admin/<int:id>/', views.DeleteAdminView.as_view(), name='deleteadmin'),
 
    path('admin-logout/', views.LogoutView.as_view(), name='admin-logout'),
    path('add-return-book-list/', user_view.AddReturnBookViewList.as_view(), name='add-return-book-list'),
    path('add-return-book/<int:id>/', views.AddReturnBookView.as_view(), name='add-return-book'),
    path('add-return-book-sucess/<int:id>/', views.AddReturnBookSucessView.as_view(), name='add-return-book-sucess'),
    path('admin-profile-ui/<int:id>/', views.AdminProfile.as_view(), name='admin-profile-ui'),
    # <--------------------------user path -------------------------->
    path('user-dash/', user_view.UserBase.as_view(), name='user'),
    path('user-profile/<int:id>/', user_view.UserProfile.as_view(), name='user-profile'),
    path('buy-book/', user_view.BuyBooks.as_view(), name='buybook'),
    path('buy-book-detail/<int:id>/', user_view.BuyBookDetail.as_view(), name='buybookdetail'),

    path('show-buy-book-table/', user_view.ShowBuyBookTable.as_view(), name='showbuybooktable'),
    path('user-logout/', user_view.LogoutView.as_view(), name='user-logout'),
    path('return-book/<int:id>/', user_view.ReturnBookView.as_view(), name='return-book'),
    # <--------------------------Api path -------------------------->
    path('api/', include('buy_book_api.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


