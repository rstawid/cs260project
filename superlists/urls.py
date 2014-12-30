from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lists.views.user_login', name='home'),
	url(r'^lists/', include('lists.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
