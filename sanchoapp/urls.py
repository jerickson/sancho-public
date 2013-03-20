from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sanchoapp.views.home', name='home'),
    # url(r'^sanchoapp/', include('sanchoapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/book/highlights/')),
    url(r'^$', RedirectView.as_view(url='book/highlights/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/', include('books.urls')),
    url(r'^lists/', include('lists.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': '/var/www/django/sancho/sanchoapp/static'}),
)
