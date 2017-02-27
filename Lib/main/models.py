from django.db import models
from django.contrib.auth.models import User as authModel 

# Create your models here.
class BookType(models.Model):
    TypeNum = models.IntegerField(primary_key=True)
    TypeName = models.CharField(max_length=20)
    def __unicode__(self):
        return '%s' % (self.TypeName)
        
class Book(models.Model):
    bookId = models.CharField(max_length = 40,primary_key= True)
    bookName = models.CharField(max_length=40)
    bookType = models.ForeignKey(BookType)
    bookPublisher = models.CharField(max_length=40)
    bookAuthor = models.CharField(max_length=50)
    bookIntroduction = models.TextField()
    bookPrice = models.IntegerField()
    def __unicode__(self):
        return '%s' % (self.bookName)
        
class BookNum(models.Model):
    bookId = models.ForeignKey(Book)
    bookNum = models.IntegerField()
    def __unicode__(self):
        return '%s' % (self.bookId.bookName)

class StaffInfo(models.Model):
    staffId = models.ForeignKey(authModel)
    staffName = models.CharField(max_length = 30)
    def __unicode__(self):
        return '%s' % (self.staffName)
        
class AddItem(models.Model):
    bookId = models.ForeignKey(Book)
    staffId = models.ForeignKey(StaffInfo)
    addNum = models.IntegerField()
    def __unicode__(self):
        return '%s' % (self.bookId.bookName)

class UserInfo(models.Model):
    userId = models.ForeignKey(authModel)
    userName = models.CharField(max_length=25)
    userSex = models.BooleanField(default = True)
    userAge = models.IntegerField()
    userPhoneNum = models.CharField(max_length=12,null=True,blank=True)
    userRegistTime = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return '%s' % (self.userName)

class BorrowItem(models.Model):
    borrowItemId = models.IntegerField(primary_key = True)
    bookId = models.ForeignKey(Book)
    staffId = models.ForeignKey(StaffInfo)
    userId = models.ForeignKey(UserInfo)
    hasReturned = models.BooleanField(default = False)
    def __unicode__(self):
        return '%s' % (self.borrowItemId)