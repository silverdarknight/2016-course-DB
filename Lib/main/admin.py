from django.contrib import admin

# Register your models here.
from .models import Book,BookType,BookNum,AddItem,BorrowItem,UserInfo,StaffInfo

admin.site.register(Book)
admin.site.register(BookType)
admin.site.register(BookNum)
admin.site.register(AddItem)
admin.site.register(BorrowItem)
admin.site.register(UserInfo)
admin.site.register(StaffInfo)