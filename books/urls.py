from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from django.views.generic import RedirectView, TemplateView
from tastypie.api import Api
from books.views import *
from books.api import PassageApiDetail, PassageListApi, DictionaryListApi

urlpatterns = patterns('',
    url(r'(?P<slug>[\w-]+)/text$', ChapterListView.as_view(), name='books.table_of_contents'),
    url(r'moby-dick/text/(?P<slug>[\w-]+)$', ChapterView.as_view(), name='books.chapter'),
    url(r'^api/dictionary/(?P<word>[\w-]+)$', DictionaryListApi.as_view()),
    url(r'^highlights/create', login_required(CreateHighlight.as_view()), name='books.highlight.create'),
    url(r'^highlights/search$', SearchHighlightListView.as_view(), name='books.highlight.search'),
    url(r'^highlights/random$', RandomHighlightView.as_view(), name='books.highlight.random'),
    url(r'^highlight/(?P<pk>[0-9]+)/like$', like_highlight, name='books.highlight.like'),
    url(r'lists/$', BookListView.as_view(), name='books.list'),
    url(r'(?P<slug>[\w-]+)$', BookDetailView.as_view(), name='books.detail'),
    url(r'^highlights/', HighlightListView.as_view(), name='books.highlight.list'),
    url(r'^dictionary/$', TemplateView.as_view(template_name="books/dictionary.html"), name='books.dictionary'),
    #url(r'^api/passages/$', PassageListApi.as_view()),
    #url(r'^api/passage/(?P<pk>[0-9]+)/$', PassageApiDetail.as_view()),
)
