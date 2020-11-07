from django.urls import path
from django.conf.urls import url
from . import views

app_name='home'

urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.login_user,name='login_user'),
    path('logout',views.logout_user,name='logout_user'),
    path('signup',views.signup,name='signup'),
    path('past',views.past_search,name='past_search'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),


]
