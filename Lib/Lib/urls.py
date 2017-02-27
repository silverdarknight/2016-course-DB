from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Lib.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^loginView/','main.views.loginView',name="loginView"),
    url(r'^registView/','main.views.registView',name="registView"),
    url(r'^logoutView/','main.views.logoutView',name="logoutView"),
    url(r'^userBorrowedBook/','main.views.userBorrowedBook',name="userBorrowedBook"),
    url(r'^staffAddBookNum/','main.views.staffAddBookNum',name="staffAddBookNum"),
    url(r'^staffCreateBook/','main.views.staffCreateBook',name="staffCreateBook"),
    url(r'^viewBook/','main.views.viewBook',name="viewBook"),
    url(r'^main/','main.views.main',name="main"),
    url(r'^regist/','main.views.regist',name="regist"),
    url(r'^login/','main.views.login',name="login"),
    url(r'^staffBorrowUserBook/','main.views.staffBorrowUserBook',name="staffBorrowUserBook"),
    url(r'^staffReturnUserBook/','main.views.staffReturnUserBook',name="staffReturnUserBook"),
    url(r'^staffChangeBookInfo/','main.views.staffChangeBookInfo',name="staffChangeBookInfo"),
    url(r'^getTypeOptions/','main.views.getTypeOptions',name="getTypeOptions"),
    url(r'^staffViewUser/','main.views.staffViewUser',name='staffViewUser'),
    url(r'^staffViewUserDetail/','main.views.staffViewUserDetail',name="staffViewUserDetail"),
)
