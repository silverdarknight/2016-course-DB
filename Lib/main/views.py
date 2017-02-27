# coding:utf-8
import json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User as authUser
from django.contrib import auth
from django.core.paginator import Paginator

from main.models import Book,BookType,BookNum,AddItem,BorrowItem,UserInfo,StaffInfo
# Create your views here.
def loginView(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return render(request,"login.html",{'msgFail':'已有用户登陆中,自动登出请重新登陆'})
    else:
        return render(request,"login.html")
def logoutView(request):
    auth.logout(request)
    return render(request,"logout.html")
    
def registView(request):
    return render(request,"regist.html")

def main(request):
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            staffInfo = StaffInfo.objects.get(staffId=currentUser)
            typeInfo = []
            for typeItem in BookType.objects.all():
                typeInfo.append({"typeNum":typeItem.TypeNum,"typeInfo":typeItem.TypeName})
            currentUserInfo = {"userId":currentUser.username,
                               "userName":staffInfo.staffName}
            return render(request,'indexStaff.html',{"currentUser":currentUserInfo,"is_staff":True,"typeList":typeInfo})#To staffMain
        else:
            return HttpResponseRedirect("/staffViewUserDetail")
    else:
        return HttpResponseRedirect("/loginView")

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect("/login")
    else:
        return HttpResponseRedirect("/login")

def regist(request):
    try:
        userid = request.POST['id']
        userpw = request.POST['pw']
        useremail = request.POST['email']
        username = request.POST['name']
        usersex = request.POST['sex']
        userage = request.POST['age']
        userpn = request.POST['phonenum']
    except:
        HttpResponseRedirect("/registView")
    try:
        user = authUser.objects.create_user(username = userid,
                                            password = userpw,
                                            email = useremail)
        user.is_staff = False
        user.save()
        try:
            UserInfo.objects.create(userId = user,
                                    userName = username,
                                    userSex = usersex,
                                    userAge = userage,
                                    userPhoneNum = userpn)
        except:
            return HttpResponse("regist fail")
        return HttpResponseRedirect("/loginView")
    except:
        return HttpResponseRedirect("/registView")

def login(request):
    try:
        userId = request.POST['id']
        userPw = request.POST['pw']
    except:
        return HttpResponseRedirect("/login")
    user = auth.authenticate(username=userId,password=userPw)
    if user is not None and user.is_active:
        auth.login(request,user)
        return HttpResponseRedirect("/main")
    else:
        return HttpResponseRedirect("/login")

def userBorrowedBook(request):#得到当前用户已借阅图书数组
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            try:
                userid = request.GET['userid']
                userInfoFK = UserInfo.objects.get(userId = authUser.objects.get(username=userid))
                borrowItems = BorrowItem.objects.filter(userId = userInfoFK)
                ansBookList = []                
                for item in borrowItems:
                    if not item.hasReturned:
                        ansBookList.append(item.bookId)
                ans = []
                for bookItem in ansBookList:
                    currentBook = {"name":bookItem.bookName,
                                   "type":bookItem.bookType.TypeName,
                                   "author":bookItem.bookAuthor,
                                   "price":bookItem.bookPrice}
                    ans.append(currentBook)
                return HttpResponse(json.dumps({"end":True,"msg":ans}),content_type="application/json")
            except:
                return HttpResponse(json.dumps({"end":False}),content_type="application/json")
        else:
            try:
                userInfoFK = UserInfo.objects.get(userId=currentUser)
                borrowItems = BorrowItem.objects.filter(userId = userInfoFK)
                ansBookList = []                
                for item in borrowItems:
                    if not item.hasReturned:
                        ansBookList.append(item.bookId)
                ans = []
                for bookItem in ansBookList:
                    currentBook = {"name":bookItem.bookName,
                                   "type":bookItem.bookType.TypeName,
                                   "author":bookItem.bookAuthor,
                                   "price":bookItem.bookPrice}
                    ans.append(currentBook)
                return HttpResponse(json.dumps({"end":True,"msg":ans}),content_type="application/json")
            except:
                return HttpResponse(json.dumps({"end":False}),content_type="application/json")
            return HttpResponse(json.dumps({"end":False}),content_type="application/json")
    else:
        return HttpResponse(json.dumps({"end":False}),content_type="application/json")

def viewBook(request):
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            staffOrNot = True
            userFK = StaffInfo.objects.get(staffId=currentUser).staffName
        else:
            staffOrNot = False
            userFK = UserInfo.objects.get(userId=currentUser).userName
        currentUserTrans = {"userId":currentUser.username,"userName":userFK}
        try:
            mode = request.GET['mode']
            startPage = request.GET['startPage']
            offset = request.GET['offset']
            bookLikeName = request.GET['bookLikeName']
        except:
            return HttpResponse("get error")
        ans = []
        if mode == 'Detail':
            BookAns = Book.objects.get(bookId=bookLikeName)#得到书的详细信息
            BookNumFK = BookNum.objects.get(bookId=BookAns)
            BookDetail = {"bookId":BookAns.bookId,
                          "bookName":BookAns.bookName,
                          "bookType":BookAns.bookType.TypeName,
                          "bookPublisher":BookAns.bookPublisher,
                          "bookAuthor":BookAns.bookAuthor,
                          "bookIntroduction":BookAns.bookIntroduction,
                          "bookPrice":BookAns.bookPrice,
                          "bookNum":BookNumFK.bookNum}
            return HttpResponse(json.dumps(BookDetail),content_type="application/json")
        elif mode == "simple":
            currentPage = int(startPage)
            if bookLikeName == '':#一连串书的信息
                BookAll = Book.objects.all().order_by("bookName")   
            else:
                BookAll = Book.objects.filter(bookName__contains=bookLikeName).order_by("bookName")  
            bookPagi = Paginator(BookAll,int(offset))
            pageN = bookPagi.page(currentPage)
            pageNum = bookPagi.page_range[-1]
            after_range_num = 5
            befor_range_num = 4
            bookAnsList = pageN.object_list
            if currentPage-1>after_range_num:
                pageList = bookPagi.page_range[currentPage-1-after_range_num:currentPage-1+befor_range_num]
            else:
                pageList = bookPagi.page_range[0:currentPage-1+befor_range_num]    
            for BookAns in bookAnsList:
                BookNumFK = BookNum.objects.get(bookId=BookAns)
                BookDetail = {"bookName":BookAns.bookName,
                              "bookId":BookAns.bookId,
                              "bookType":BookAns.bookType.TypeName,
                              "bookPublisher":BookAns.bookPublisher,
                              "bookAuthor":BookAns.bookAuthor,
                              "bookPrice":BookAns.bookPrice,
                              "bookNum":BookNumFK.bookNum,
                              "bookIntroduction":BookAns.bookIntroduction[:60]}
                ans.append(BookDetail)
            return render(request,'library.html',{"currentUser":currentUserTrans,"is_staff":staffOrNot,"bookList":ans,"bookLikeName":bookLikeName,"pageList":pageList,"currentPage":currentPage,"nextPage":currentPage+1,"prevPage":currentPage-1,"endPage":pageNum})
    else:
        return HttpResponseRedirect("/login")

def staffCreateBook(request):#添加Book信息，添加BookNum=0
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            if currentUser.has_perms(["main.add_additem","main.add_booknum"]):
                try:
                    bookid = request.GET['bookid']
                    bookname = request.GET['bookname']
                    booktype = request.GET['booktype']
                    bookpublisher = request.GET['bookpublisher']
                    bookauthor = request.GET['bookauthor']
                    bookintroduction = request.GET['bookintroduction']
                    bookprice = request.GET['bookprice']
                    booknum = request.GET['booknum']
                except:
                    return HttpResponse('get error')
                bookTypeFK = BookType.objects.get(TypeNum=booktype)
                createBook = Book.objects.create(bookId=bookid,
                                    bookName=bookname,
                                    bookType=bookTypeFK,
                                    bookPublisher=bookpublisher,
                                    bookAuthor=bookauthor,
                                    bookIntroduction=bookintroduction,
                                    bookPrice=bookprice)
                BookNum.objects.create(bookId=createBook,
                                       bookNum=booknum)
                AddItem.objects.create(bookId=createBook,
                                       staffId=StaffInfo.objects.get(staffId=currentUser),
                                       addNum=booknum)
                return HttpResponse("success!!!")
        else:
            return HttpResponse("you do not have this perm")
    else:
        return HttpResponse("login Page,you are not login already")

def staffAddBookNum(request):#已存在Book类，添加addItem 更改或添加BookNum
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            if currentUser.has_perms(["main.add_additem","main.change_additem","main.add_booknum","main.change_booknum"]):
                try:
                    try:
                        bookid = request.GET['bookid']
                        addBookNum = request.GET['addBookNum']
                    except:
                        return HttpResponse(bookid)
                    BookFK = Book.objects.get(bookId=bookid)
                    staffInfoFK = StaffInfo.objects.get(staffId=currentUser)
                    AddItem.objects.create(bookId=BookFK,staffId=staffInfoFK,addNum=addBookNum)
                    try:
                        changeBookNum = BookNum.objects.get(bookId__bookId=bookid)
                        changeBookNum.bookNum += int(addBookNum)
                        changeBookNum.save()
                    except:
                        BookNum.objects.create(bookId=BookFK,bookNum=addBookNum)
                    return HttpResponse("add success!")
                except:
                    return HttpResponse('error GET')
            else:
                return HttpResponse("you do not have this perm")
        else:
            auth.logout(request)
            return HttpResponse("you are not staff")
    else:
        return HttpResponse("login Page,you are not login already")

def staffBorrowUserBook(request):
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            if currentUser.has_perms(["main.add_borrowitem",'main.change_booknum']):
                try:
                    bookid = request.GET['bookid']
                    userid = request.GET['userid']
                except:
                    return HttpResponse('get error')
                bookNumItem = BookNum.objects.get(bookId__bookId=bookid)
                if bookNumItem.bookNum==0:
                    return HttpResponse("no more book avalible")
                borrowitemsNum = len(BorrowItem.objects.all())
                borrowitems = BorrowItem.objects.create(borrowItemId=borrowitemsNum+1,
                                                        bookId=Book.objects.get(bookId=bookid),
                                                        staffId=StaffInfo.objects.get(staffId=currentUser),
                                                        userId=UserInfo.objects.get(userId__username=userid),
                                                        hasReturned=False)
                bookNumItem.bookNum -= 1
                bookNumItem.save()
                return HttpResponse(json.dumps({'end':True}),content_type="application/json")
            else:
                return HttpResponse("has no perm")
        else:
            return HttpResponse("you have no perm")
    else:
        return HttpResponse("login Page,you are not login already")

def staffReturnUserBook(request):
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            if currentUser.has_perms(["main.change_borrowitem"]):
                try:
                    bookid = request.GET['bookid']
                    userid = request.GET['userid']
                except:
                    return HttpResponse('get error')
                bookNumItem = BookNum.objects.get(bookId__bookId=bookid)
                borrowitems = BorrowItem.objects.filter(bookId__bookId=bookid,userId__userId__username=userid).exclude(hasReturned=True)
                if len(borrowitems)==0:
                    return HttpResponse("you have not borrow this book")
                for borrowitem in borrowitems:
                    if borrowitem.hasReturned:
                        continue
                    else:
                        borrowitem.hasReturned = True
                        borrowitem.save()
                        bookNumItem.bookNum += 1
                bookNumItem.save()
                return HttpResponse(json.dumps({'end':True}),content_type="application/json")
            else:
                return HttpResponse("has no perm")
        else:
            return HttpResponse("you have no perm")
    else:
        return HttpResponse("login Page,you are not login already")
def getTypeOptions(request):
    if request.user.is_authenticated():
        ans=[]
        options = BookType.objects.all()
        for option in options:
            ans.append({"num":option.TypeNum,"optionName":option.TypeName})
        return HttpResponse(json.dumps(ans),content_type="application/json")
    else:
        return HttpResponse("login Page,you are not login already")
def staffViewUserDetail(request):
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            try:
                userid = request.GET['userid']
            except:
                return HttpResponseRedirect('/main')
            currentLoginUser = {'userId':currentUser.username,
                                'userName':StaffInfo.objects.get(staffId=currentUser).staffName}
            userAuth = authUser.objects.get(username=userid)
            userInfoFK = UserInfo.objects.get(userId=userAuth)
            borrowList = BorrowItem.objects.filter(userId=userInfoFK).order_by('borrowItemId')
            userinfo = {'userid':userAuth.username,
                        'username':userInfoFK.userName,
                        'email':userAuth.email,
                        'sex':userInfoFK.userSex,
                        'age':userInfoFK.userAge,
                        'pn':userInfoFK.userPhoneNum,
                        'time':userInfoFK.userRegistTime.strftime('%Y-%m-%d')}
            borrowInfoList = []
            for i,borrowItem in enumerate(borrowList):
                borrowInfoList.append({'bookName':borrowItem.bookId.bookName,
                                       'itemNum':i+1,
                                       'staffId':borrowItem.staffId.staffId.username,
                                       'hasReturn':borrowItem.hasReturned})
            borrowInfoList.reverse()
            return render(request,'userDetail.html',{'userInfo':userinfo,'borrowList':borrowInfoList,'currentUser':currentLoginUser,'is_staff':True})
        else:
            userid = currentUser.username
            currentLoginUser = {'userId':currentUser.username,
                                'userName':UserInfo.objects.get(userId=currentUser).userName}
            userAuth = authUser.objects.get(username=userid)
            userInfoFK = UserInfo.objects.get(userId=userAuth)
            borrowList = BorrowItem.objects.filter(userId=userInfoFK).order_by('borrowItemId')
            userinfo = {'userid':userAuth.username,
                        'username':userInfoFK.userName,
                        'email':userAuth.email,
                        'sex':userInfoFK.userSex,
                        'age':userInfoFK.userAge,
                        'pn':userInfoFK.userPhoneNum,
                        'time':userInfoFK.userRegistTime.strftime('%Y-%m-%d')}
            borrowInfoList = []
            for i,borrowItem in enumerate(borrowList):
                borrowInfoList.append({'bookName':borrowItem.bookId.bookName,
                                       'itemNum':i+1,
                                       'staffId':borrowItem.staffId.staffId.username,
                                       'hasReturn':borrowItem.hasReturned})
            borrowInfoList.reverse()
            return render(request,'userDetail.html',{'userInfo':userinfo,'borrowList':borrowInfoList,'currentUser':currentLoginUser,'is_staff':False})
    else:
        return HttpResponseRedirect("/login")
    
def staffViewUser(request):
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            try:
                username = request.GET['username']
                offset = request.GET['offset']
                startPage = request.GET['startPage']
            except:
                return HttpResponse('startPage get error')
            currentPage = int(startPage)
            if username == '':
                scanUser = UserInfo.objects.all().order_by('userName')
            else:
                scanUser = UserInfo.objects.filter(userName__contains = username)
            userPagi = Paginator(scanUser,int(offset))
            pageN = userPagi.page(currentPage)
            after_range_num = 5
            befor_range_num = 4
            scanUserList = pageN.object_list
            ansUserList = []
            for userItem in scanUserList:
                ansUserList.append({'userid':userItem.userId.username,
                                    'username':userItem.userName,
                                    'usersex':userItem.userSex,
                                    'userage':userItem.userAge})
            if currentPage-1>after_range_num:
                pageList = userPagi.page_range[currentPage-1-after_range_num:currentPage-1+befor_range_num]
            else:
                pageList = userPagi.page_range[0:currentPage-1+befor_range_num]
            ans = {'userList':ansUserList,'pageList':pageList,'currentPage':currentPage}
            return HttpResponse(json.dumps(ans),content_type="application/json")
        else:
            return HttpResponse('not staff')
    else:
        return HttpResponse('not login')

def staffChangeBookInfo(request):
    if request.user.is_authenticated():
        currentUser = request.user
        if currentUser.is_staff:
            if currentUser.has_perms(["main.change_book","main.change_booknum"]):
                try:
                    bookid = request.GET['bookid']
                    bookname = request.GET['bookname']
                    booktype = request.GET['booktype']
                    bookpub = request.GET['bookpublisher']
                    bookauthor = request.GET['bookauthor']
                    bookintro = request.GET['bookintroduction']
                    bookprice = request.GET['bookprice']
                    booknum = request.GET['booknum']
                except:
                    return HttpResponse("get error")
                bookFK = Book.objects.get(bookId=bookid)
                bookNumFK = BookNum.objects.get(bookId__bookId=bookid)
                bookFK.bookName = bookname
                bookFK.bookType = BookType.objects.get(TypeNum=booktype)
                bookFK.bookPublisher = bookpub
                bookFK.bookAuthor = bookauthor
                bookFK.bookIntroduction = bookintro
                bookFK.bookPrice = bookprice
                bookFK.save()
                bookNumFK.bookNum = booknum
                bookNumFK.save()
                return HttpResponse("success!")
            else:
                return HttpResponse("has no perm")
        else:
            return HttpResponse("you have no perm")
    else:
        return HttpResponse("login Page,you are not login already")