from django.conf.urls import url, include
from wall_app import views


accountpatterns = [
    url(r'^login/$', views.account_login, name='account_login'),
    url(r'^logout/$', views.account_logout, name='account_logout'),
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/', include(accountpatterns)),
]
