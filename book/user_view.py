from django.shortcuts import render,redirect
from .models import Book,Buybook
from django.contrib.auth.models import User,auth
from django.contrib import messages
import re
from datetime import date,datetime
from django.http import JsonResponse

import os
# Create your views here.
from django.views import View
from django.shortcuts import  render,redirect
from .models import Buybook,Book


class UserBase(View):
    def get(self,request):
        if request.user.is_authenticated:
            dates=date.today()
            return render(request,'userbase.html',{'date':dates})
        else:
            return redirect('login')

class BuyBooks(View):
    def get(self,request):
        if request.user.is_authenticated:
            book=Book.objects.filter(deleted=False)
            print(date.today())
            return render(request,'buybook.html',{'book':book, 'date':date.today()})
        else:
            return redirect('login')

class BuyBookDetail(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            if Book.objects.filter(pk=id).exists():
                book=Book.objects.get(pk=id)
                counter=int(book.bookquantity)
                return render(request,'buybookdetail.html',{'book':book,'date':date.today(),'counter':range(1,counter+1)})
            else:
                return redirect('buybook')
        else:
            return redirect('login')

    def post(self,request,id):
        if Book.objects.filter(pk=id).exists():
            books=Book.objects.get(pk=id)
            username=request.POST['username']
            phone=request.POST['phone']
            returndate=request.POST['returndate']
            buybookquantity=request.POST['buybookquantity']
            if buybookquantity == 'How many book You are buying?':
                messages.info(request, 'Enter the book quantity..')
                return redirect('buybookdetail',id=id)
            if phone == '':
                messages.info(request, 'Enter the phone number..')
                return redirect('buybookdetail',id=id)
            else:
                phonerex = re.compile(r"[0-9]+")
                if (re.search(phonerex, phone)) :
                    if len(phone)>10:
                        messages.info(request, 'Phone Number is only 10 digits..')
                        return redirect('buybookdetail', id=id)
                    else:
                        Buybook.objects.create(bookdetail=books, username=username, buydate=date.today(),returndate=returndate,buybookquantity=buybookquantity, buy=True,
                                               deleted=False, phone=phone)
                        buyquantity = int(buybookquantity)
                        bookquantity = int(books.bookquantity) - buyquantity
                        books.bookquantity = str(bookquantity)
                        if bookquantity == 0:
                            books.deleted = True
                            books.save()
                        else:
                            books.deleted = False
                            books.save()
                        bookname = books.bookname
                        authername = books.authername
                        bookpage = books.bookpage
                        bookprice = books.bookprice
                        booklanguage = books.booklanguage
                        buydate=date.today()
                        return render(request, 'showbuybookdetail.html',
                                      {'bookname': bookname, 'authername': authername, 'bookpage': bookpage,
                                       'bookprice': bookprice, 'booklanguage': booklanguage, 'username': username,'buybookquantity':buybookquantity,
                                       'phone': phone,'buydate':buydate,'returndates':returndate,'date':date.today()})

                else:
                    messages.info(request, 'Phone Number Not Valid..')
                    return redirect('buybookdetail',id=id)
        else:
            return redirect('buybook')

class ShowBuyBookTable(View):
    def get(self, request):
        if request.user.is_authenticated:
            book = Buybook.objects.filter(username=request.user.username,deleted=False)
            print(request.user)
            return render(request, 'showbuybooktable.html',{'book':book,'date':date.today()})
        else:
            return redirect('login')
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
                auth.logout(request)
                return redirect('login')
        else:
                return redirect('login')

class ReturnBookView(View):
    def get(self, request,id):
        if request.user.is_authenticated:
            if Buybook.objects.filter(pk=id).exists():
                buybook=Buybook.objects.get(pk=id)
                buybook.deleted=True
                buybook.save()
                return JsonResponse({'data':'done'})
            else:
                return redirect('buybook')
        else:
            return redirect('login')

class  AddReturnBookViewList(View):
    def get(self, request):
        if request.user.is_authenticated:
            buybook = Buybook.objects.filter(deleted=True)
            return render(request,'Return_book_list.html',{'buybook':buybook,'date':date.today()})
        else:
                return redirect('login')

class  UserProfile(View):
    def get(self, request,id):
        if request.user.is_authenticated:
            print(id)
            return render(request,'userprofile.html',{'date':date.today()})
        else:
            return redirect('login')

    def post(self, request,id):
        if User.objects.filter(id=id).exists():
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            if not first_name or not last_name or not email:
                messages.info(request, 'fields are required')
                return redirect('user-profile', id=id)
            User.objects.filter(pk=id).update(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            messages.success(request, 'Your data hase been updated')
            return redirect('user-profile', id=id)
        messages.info(request, f"User '{id}' does not exist")
        return redirect('user-profile', id=id)

