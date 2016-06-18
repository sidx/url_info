from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getUrlData$', views.getUrlData, name='getUrlData'),
    url(r'^printUrlData$', views.printUrlData, name='printUrlData'),
]
