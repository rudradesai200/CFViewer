"""apiuse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf.urls import handler404
from core.viewers.renderviews import *
from core.viewers.adminviews import *
from core.viewers.staticviews import *

urlpatterns = [
    url(r'^dashboard/',dashboard,name="dashboard"),
    url(r'^showbooks/',showbooks,name="books"),
    url(r'^subs/(?P<handle>.*)/(?P<contid>.*)/',submissionsviewer,name="subsviewer"),
    url(r'^problems/',problems,name="problems"),
    url(r'^contests/',contests,name="contests"),
    url(r'^friends/',friendsunsolved,name="friendsunsolved"),
    url(r'^suggest/(?P<slug>.*)/',suggestor,name="suggestor"),
    url(r'^pluginload/(?P<slug>.*)/(?P<handle>.*)/',plugin_load,name="plugin_suggestor"),
    # url(r'^invite/(?P<handle>.*)/',foobarinvite,name="foobarinvite"),
    # url(r'^change/(?P<handle>.*)/(?P<stat>.*)/',acceptinvite,name="invitestatuschange"),
    # url(r'^adspage/',adspage,name="adspage"),
    url(r'^',home,name="home"),
]

handler404 = 'core.viewers.staticviews.error_404_view'