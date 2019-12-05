from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    # path("index", views.index,name="index"),
    path("", views.index, name="index"),
    path("maps", views.maps, name="maps"),
    path("getlocation", views.getlocation, name="getlocation"),
    path("book_a_locker", views.book_a_locker, name="book_a_locker"),
    path("is_subscribed", views.is_subscribed, name="is_subscribed"),
    path("publish_to_station", views.publish_to_station, name="publish_to_station"),
    # path('auth', views.authenticate, name='authenticateuser'),
]
