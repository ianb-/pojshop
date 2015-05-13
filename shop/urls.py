from django.conf.urls import patterns, url
from shop import views

urlpatterns = patterns('',
	url(r'^$', views.front, name="frontpage"),
	url(r'^c/(?P<category_slug>[\w\-]+)/$', views.category, name="category"),
    url(r'^c/(?P<category_slug>[\w\-]+)/(?P<pg>\d+)', views.category, name="category"),
    url(r'^p/(?P<product_slug>[\w\-]+)/$', views.product, name="product"),
    url(r'^addtotrolley/', views.add_to_trolley, name="add_to_trolley"),
    url(r'^removefromtrolley/', views.remove_from_trolley, name="remove_from_trolley"),
    url(r'^emptytrolley/', views.empty_trolley, name="emptytrolley"),
    url(r'^trolley/', views.trolley, name="trolley"),
    url(r'^checkout/', views.checkout, name="checkout"),
    url(r'^history/', views.history, name="history"),
    url(r'^order/(?P<order_id>[\w\-]+)/$', views.order, name="order"),
	)