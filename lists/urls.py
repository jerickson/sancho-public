from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from books.views import *

urlpatterns = patterns('',
    url(r'item/(?P<id>\d+)/move-up$', 'lists.views.move_item_up', name='move_item_up'),
    url(r'item/(?P<id>\d+)/move-down$', 'lists.views.move_item_down', name='move_item_down'),
)

