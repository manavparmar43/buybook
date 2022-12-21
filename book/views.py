from django.contrib.auth.models import auth
from book.models import User
from django.contrib import messages
import re
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from .models import Buybook, Book
from datetime import date
 
class AdminBaseView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, 'base.html',{'date':date.today()})
            else:
                return redirect('user')
        else:
            return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        usernames = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=usernames, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('base')
            else:
                return redirect('user')
        else:

            messages.info(request, 'Invalid input')
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                auth.logout(request)
                return redirect('login')
            else:
                return redirect('login')
        else:
            return redirect('login')

class UserRegisterView(View):
    def get(self, request):
        return render(request, 'userregister.html',{'date':date.today()})

    def post(self, request):
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        phone=request.POST['phone']
        confirmpass = request.POST['confirmpassword']
        if firstname == '' or lastname == '' or email == '' or username == '' or password == '' or confirmpass == '' or phone == '':
            messages.info(request, 'One Filed is Empty..')
            return redirect('userregister')

        if password == confirmpass:
            pat = re.compile(r"[A-Za-z]+")
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            phonereg = re.compile(r"[0-9]+")
            if firstname != '':
                if re.fullmatch(pat, firstname):
                    pass
                else:
                    messages.info(request, 'First Name Not Valid..')
                    return redirect('userregister')
            if lastname != '':
                if re.fullmatch(pat, lastname):
                    pass
                else:
                    messages.info(request, 'Last Name Not Valid..')
                    return redirect('userregister')
            if email != '':
                if (re.search(regex, email)):
                    pass
                else:
                    messages.info(request, 'Email Not Valid..')
                    return redirect('userregister')
            if phone != '':
                if (re.search(phonereg, phone)):
                    pass
                else:
                    messages.info(request, 'Phone Number Not Valid..')
                    return redirect('userregister')
            if User.objects.filter(phone=phone).exists():
                messages.info(request, 'Phone number is Already Taken..')
                return redirect('userregister')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is Already Taken..')
                return redirect('userregister')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is Already Taken..')
                return redirect('userregister')
            if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
                messages.info(request, 'Username and Email is Already Taken..')
                return redirect('userregister')
            else:
                user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email,
                                                username=username, password=password,phone=phone,is_student=True,is_staff=False,
                                                     is_superuser=False,is_admin=False)
                user.save()
                return render(request, 'userregistersucess.html',{'date':date.today()})

        else:
            messages.info(request, 'Password not match ..')
            return redirect('userregister')


class AllUserRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, 'adminregister.html',{'date':date.today()})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request):
        firstname = request.POST['firstname']

        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        phone=request.POST['phone']
        choice=request.POST['choice']
        confirmpass = request.POST['confirmpassword']
        if firstname == '' or lastname == '' or email == '' or username == '' or password == '' or confirmpass == ''or choice=='' or choice == 'Select Choice' or phone == '':
            messages.info(request, 'One Filed is Empty..')

            return redirect('user-register')

        if password == confirmpass:
            pat = re.compile(r"[A-Za-z]+")
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            phonereg = re.compile(r"[0-9]+")
            if firstname != '':
                if re.fullmatch(pat, firstname):
                    pass
                else:
                    messages.info(request, 'First Name Not Valid..')
                    return redirect('user-register')
            if lastname != '':
                if re.fullmatch(pat, lastname):
                    pass
                else:
                    messages.info(request, 'Last Name Not Valid..')
                    return redirect('user-register')
            if email != '':
                if (re.search(regex, email)):
                    pass
                else:
                    messages.info(request, 'Email Not Valid..')
                    return redirect('user-register')
            if phone != '':
                if (re.search(phonereg, phone)):
                    pass
                else:
                    messages.info(request, 'Phone Number Not Valid..')
                    return redirect('user-register')
            if User.objects.filter(phone=phone).exists():
                messages.info(request, 'Phone is Already Taken..')
                return redirect('user-register')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is Already Taken..')
                return redirect('user-register')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is Already Taken..')
                return redirect('user-register')
            if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
                messages.info(request, 'Username and Email is Already Taken..')
                return redirect('user-register')
            else:
                if choice == 'student':
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email,
                                                     username=username, password=password, phone=phone,is_student=True,is_staff=False,
                                                     is_superuser=False,is_admin=False)
                    user.save()
                else:
                    user = User.objects.create_superuser(first_name=firstname, last_name=lastname, email=email,
                                                    username=username, password=password, phone=phone,is_student=False)
                    user.save()

                messages.success(request, 'Your data has been saved..')
                return redirect('user-register')
        else:
            messages.info(request, 'Password not match ..')
            return redirect('user-register')
class Forgotpasswordview(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, 'forgot-password.html')
            else:
                return redirect('login')
        else:
            return redirect('login')
class AddBookView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, 'addbook.html',{'date':date.today()})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request):
        bookname = request.POST['bookname']
        authername = request.POST['authername']
        bookpage = request.POST['bookpage']
        bookprice = request.POST['bookprice']
        booklanguage = request.POST['booklanguage']
        bookquantity = request.POST['bookquantity']
        if bookname == '' or authername == '' or bookpage == '' or bookprice == '' or booklanguage == '' or bookquantity == '':
            messages.info(request, 'One Filed is Empty..')
            return redirect('addbook')

        else:
            bookpat = re.compile(r"[A-Za-z0-9]+")
            autherpat = re.compile(r"[A-Za-z]+")
            book = re.compile(r"[0-9]+")
            if bookname != '':
                if re.fullmatch(bookpat, bookname):
                    pass
                else:
                    messages.info(request, 'Book Name Not Valid..')
                    return redirect('addbook')
            if authername != '':
                if re.fullmatch(autherpat, authername):
                    pass
                else:
                    messages.info(request, 'Auther Name Not Valid..')
                    return redirect('addbook')
            if bookpage != '':
                if (re.search(book, bookpage)):
                    pass
                else:
                    messages.info(request, 'Book Page Not Valid..')
                    return redirect('addbook')
            if bookquantity != '':
                if (re.search(book, bookquantity)):
                    pass
                else:
                    messages.info(request, 'Book Quantity Not Valid..')
                    return redirect('addbook')
            if bookprice != '':
                if (re.search(book, bookprice)):
                    pass
                else:
                    messages.info(request, 'Book Price Not Valid..')
                    return redirect('addbook')
            if booklanguage != '':
                if (re.search(autherpat, booklanguage)):
                    pass
                else:
                    messages.info(request, 'Book language Not Valid..')
                    return redirect('addbook')

            if Book.objects.filter(bookname=bookname).exists():
                messages.info(request, 'Book name Already Taken..')
                return redirect('addbook')

            else:
                bookprices = int(bookprice)
                bookpages = int(bookpage)

                Book.objects.create(bookname=bookname, bookquantity=bookquantity, bookprice=bookprices,
                                    bookpage=bookpages,
                                    authername=authername, booklanguage=booklanguage, deleted=False)
                messages.success(request, 'Your book has been added...')
                return redirect('addbook')
class ShowBookTableView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                book = Book.objects.all()

                return render(request, 'showbooktable.html', {'book': book,'date':date.today()})
            else:
                return redirect('login')
        else:
            return redirect('login')
class RegisterUserTableView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                userlist = []
                user = User.objects.all()
                for i in user:
                    if i.is_superuser != True:
                        userlist.append(i)
                return render(request, 'register_user_table.html', {'user': userlist,'date':date.today()})
            else:
                return redirect('login')
        else:
            return redirect('login')

class RegisterAdminTableView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                adminlist = []
                user = User.objects.all()
                for i in user:
                    if i.is_superuser == True:
                        adminlist.append(i)
            else:
                return redirect('login')
        else:
            return redirect('login')

        return render(request, 'register_admin_table.html', {'admin': adminlist,'date':date.today()})

class EditBookView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                if Book.objects.filter(pk=id).exists():
                    book = Book.objects.get(pk=id)
                    return render(request, 'editbook.html', {'book': book,'date':date.today()})
                else:
                    messages.error(request,'Book not found...')
                    return redirect('showbooktable')
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request, id):
        book = Book.objects.get(pk=id)

        book.bookname = request.POST['bookname']
        book.authername = request.POST['authername']
        book.bookpage = request.POST['bookpage']
        book.bookprice = request.POST['bookprice']
        book.booklanguage = request.POST['booklanguage']
        book.bookquantity = request.POST['bookquantity']
        if book.bookname == '' or book.authername == '' or book.bookpage == '' or book.bookprice == '' or book.booklanguage == '':
            messages.info(request, 'One Filed is Empty..')
            return redirect('editbook', id=book.id)

        else:
            bookpat = re.compile(r"[A-Za-z0-9]+")
            autherpat = re.compile(r"[A-Za-z]+")
            bookss = re.compile(r"[0-9]+")

            if book.bookname != '':
                if re.fullmatch(bookpat, book.bookname):
                    pass
                else:
                    messages.info(request, 'Book Name Not Valid..')
                    return redirect('editbook', id=book.id)
            if book.authername != '':
                if re.fullmatch(autherpat, book.authername):
                    pass
                else:
                    messages.info(request, 'Auther Name Not Valid..')
                    return redirect('editbook', id=book.id)
            if book.bookpage != '':
                if (re.search(bookss, book.bookpage)):
                    pass
                else:
                    messages.info(request, 'Book Page Not Valid..')
                    return redirect('editbook', id=book.id)
            if book.bookquantity != '':
                if (re.search(bookss, book.bookquantity)):
                    pass
                else:
                    messages.info(request, 'Book Quantity Not Valid..')
                    return redirect('editbook', id=book.id)
            if book.bookprice != '':
                if (re.search(bookss, book.bookprice)):
                    pass
                else:
                    messages.info(request, 'Book Price Not Valid..')
                    return redirect('editbook', id=book.id)
            if book.booklanguage != '':
                if (re.search(autherpat, book.booklanguage)):
                    pass
                else:
                    messages.info(request, 'Book language Not Valid..')
                    return redirect('editbook', id=book.id)

                bookprices = int(book.bookprice)
                bookpages = int(book.bookpage)
                Book.objects.update(bookname=book.bookname, bookquantity=book.bookquantity, bookprice=bookprices,
                                    bookpage=bookpages,
                                    authername=book.authername, booklanguage=book.booklanguage, deleted=False)

                messages.success(request, 'Book has been updated..')
                return redirect('editbook', id=book.id)

class DeleteBookView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                if Book.objects.filter(pk=id).exists():
                    book = Book.objects.get(pk=id)
                    book.delete()
                    return JsonResponse({'data': "done"})
                else:
                    return redirect('showbooktable')
            else:
                return redirect('login')
        else:
            return redirect('login')

class DeleteUserView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                if User.objects.filter(pk=id).exists():
                    user = User.objects.get(pk=id)
                    user.delete()
                    return redirect('registerusertable')
                else:
                    return redirect('registerusertable')
            else:
                return redirect('login')
        else:
            return redirect('login')

class DeleteAdminView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                if User.objects.filter(pk=id).exists():
                    user = User.objects.get(pk=id)
                    user.delete()
                    return redirect('registerusertable')
                else:
                    return redirect('registerusertable')
            else:
                return redirect('login')
        else:
            return redirect('login')

class BuyBookUserTableView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                buybook=Buybook.objects.filter(deleted=False)
                return render(request, 'buybookusertable.html',{'buybook':buybook,'date':date.today()})
            else:
                return redirect('login')
        else:
            return redirect('login')

class AddReturnBookView(View):
    def get(self, request,id):
        if request.user.is_authenticated:
            buybook = Buybook.objects.get(pk=id)
            buybook.deleted=True
            buybook.save()
            return JsonResponse({'data':'done'})
        else:
                return redirect('login')

class AddReturnBookSucessView(View):
    def get(self, request,id):
        if request.user.is_authenticated:
            if Buybook.objects.filter(pk=id).exists():
                buybook = Buybook.objects.get(pk=id)
                book=Book.objects.get(id=buybook.bookdetail.id)

                book.bookquantity=int(book.bookquantity)+int(buybook.buybookquantity)
                book.deleted=False
                book.save()
                buybook.delete()
                messages.success(request,'Your Book hase been added')
                return redirect('add-return-book-list')
            else:
                return redirect('base')
        else:
                return redirect('login')

class  AdminProfile(View):
    def get(self, request,id):
        if request.user.is_authenticated:
            print(id)
            return render(request,'adminprofile.html',{'date':date.today()})
        else:
            return redirect('login')

    def post(self, request, id):
        if User.objects.filter(id=id).exists():
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            if not first_name or not last_name or not email:
                messages.info(request, 'fields are required')
                return redirect('admin-profile-ui', id=id)
            User.objects.filter(pk=id).update(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            messages.success(request, 'Your data hase been updated')
            return redirect('admin-profile-ui', id=id)
        messages.info(request, f"User '{id}' does not exist")
        return redirect('admin-profile-ui', id=id)



