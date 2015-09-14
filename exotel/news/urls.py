from django.conf.urls import include, url
from . import views

urlpatterns = [

    url(r'^$',views.index, name = 'home'),
    url(r'^submit/', views.submit, name='submit'),
    url(r'^upvote/', views.upvote, name='upvote'),
    url(r'^gettitle/', views.gettitle, name='gettitle'),
]
