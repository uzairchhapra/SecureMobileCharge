from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    # path("index", views.index,name="index"),
    path("", views.index, name="index"),
    path("maps", views.maps, name="maps"),

]
