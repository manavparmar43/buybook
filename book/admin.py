from django.contrib import admin
from django.contrib.admin import ModelAdmin

from book.models import Book,Buybook


from book.models import User


class UserAdmin(ModelAdmin):
        list_display = ('id', 'email', 'username', 'first_name', 'last_name','phone' ,'is_admin','is_student')
        list_filter = ('is_admin','is_superuser','is_student')
        fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'username','is_student','phone')}),
                ('Permissions', {'fields': ('is_admin','is_superuser')}),
        )

        add_fieldsets = (
                (None, {
                        'classes': ('wide',),
                        'fields': ( 'is_student','phone'),
                }),
        )
        search_fields = ('username',)
        ordering = ('id',)
        filter_horizontal = ()


admin.site.register(User, UserAdmin)


@admin.register(Book)
class Books(admin.ModelAdmin):
        list_display=['id','bookname','bookprice','bookpage','authername','booklanguage','bookquantity','deleted']

@admin.register(Buybook)
class Buybooks(admin.ModelAdmin):
        list_display=['id','bookdetail','username','buydate','returndate','buy','phone','deleted']


# Register your models here.
