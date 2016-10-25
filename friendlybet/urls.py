"""friendlybet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from casino import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/$', views.login_page, name='login'),
    url(r'^login-user/$', views.login_user, name='login_user'),
    url(r'^logout-user/$', views.logout_user, name='logout_user'),
    url(r'^bet/$', views.bet_list, name='bet_list'),
    url(r'^bet/(?P<pk>\d+)/$', views.bet_details, name='bet_details'),
    url(r'^bet/new/$', views.bet_new, name='bet_new'),
    url(r'^bet/(?P<pk>\d+)/edit/$', views.bet_edit, name='bet_edit'),
    url(r'^fetch/$', views.fetch_games),
    url(r'^feed/$', views.populate_user_feed, name='user_feed'),
    url(r'^userpage/$', views.user_page, name='user_page'),
    url(r'^user/(?P<pk>\d+)/$', views.ext_user_page, name='ext_user_page'),
    url(r'^initeams/$', views.init_teams),
    url(r'^clean/$', views.clean_db),
    url(r'^initform/$', views.init_form),
    url(r'^team/(?P<pk>\d+)/$', views.team_page, name='team_page'),
    url(r'^activate-user/(?P<activation_key>\w+)/$', views.activate_user),
    url(r'^signup/$', views.signup_page, name='signup'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^place-bet/$', views.place_bet, name='place_bet'),
    url(r'^match-distribution/$', views.match_distribution, name='match_distribution'),
]

urlpatterns += staticfiles_urlpatterns()
