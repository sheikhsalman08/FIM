"""FIM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

from enter.views import enter,logInRegisterUser
from users.views import delete_account,update_settings, update_password,User_profile
from post.views import main_page,SinglePost
# from users.views import user_profile

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^enter/$', logInRegisterUser, name="enter"),
    url(r'^logout/$',logout,{'next_page':'enter'}, name='logout'),
    url(r'^byeforever/$',delete_account, name='byeforever'),
    url(r'^settings/$',update_settings, name='settings'),
    url(r'^settings/update_password$',update_password, name='update_password'),
    url(r'^$',main_page,name="home"),
    url(r'^post/(?P<pk>[-\w]+)/$', login_required(SinglePost.as_view()), name= 'single_post'),
    url(r'^user/(?P<pk>[-\w]+)/$', login_required(User_profile.as_view()), name= 'user_profile'),


    # url(r'^settingss/$', settingss, name='settings'),
    # url(r'^settingss/password/$', password, name='password'),
    
    url(r'^oauth/', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)