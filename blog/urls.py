from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^new/', views.new, name="new"),
	url(r'^(?P<article_slug>[\w\-]+)/$', views.article, name="article"),
	)