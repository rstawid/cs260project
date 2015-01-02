from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'lists.views.user_login', name='login'),
	url(r'^register/$', 'lists.views.register', name='register'),
	url(r'^login/$', 'lists.views.user_login', name='login'),
	url(r'^logout/$', 'lists.views.user_logout', name='logout'),
	url(r'^(?P<username>[\w\-]+)/add_item$', 'lists.views.add_item', name='add_item'),
	url(r'^(?P<username>[\w\-]+)/change_item$', 'lists.views.change_item', name='change_item'),
	url(r'^(?P<username>[\w\-]+)/$', 'lists.views.view_user_list', name='username_list'),

)
