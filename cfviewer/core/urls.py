"""apiuse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.conf.urls import handler404
from core.viewers.renderviews import *
from core.viewers.staticviews import *

urlpatterns = [
    re_path('dashboard/(?P<handle>[^/]*)/',dashboard,name="dashboard"),
    re_path('showbooks/(?P<handle>[^/]*)/',showbooks,name="books"),
    re_path('subs/(?P<handle>[^/]*)/(?P<contid>[^/]*)/',submissionsviewer,name="subsviewer"),
    re_path('problems/(?P<handle>[^/]*)/',problems,name="problems"),
    re_path('contests/(?P<handle>[^/]*)/',contests,name="contests"),
    path('friends/',friendsunsolved,name="friendsunsolved"),
    re_path('suggest/(?P<handle>[^/]*)/(?P<slug>[^/]*)/',suggestor,name="suggestor"),
    path('',home,name="home"),
]

handler404 = 'core.viewers.staticviews.error_404_view'