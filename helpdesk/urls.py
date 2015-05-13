from django.conf.urls import patterns, url
from helpdesk import views

urlpatterns = patterns('',
	url(r'^$', views.contact, name="contact"),
	url(r'^ticket/(?P<ref>[\w\-]+)/$', views.ticket, name="ticket"),
	url(r'^ticket/(?P<ref>[\w\-]+)/delete', views.delete_ticket, name="delete_ticket"),
	url(r'^ticket/(?P<ref>[\w\-]+)/edit', views.change_ticket_status, name="change_status"),
	)