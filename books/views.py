# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.utils.html import escape
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Author, Book, Passage, Chapter
from .forms import PassageForm
from lists.models import ItemList


class BookDetailView(DetailView):

    model = Book
    template_name = "books/book_detail.html"

    def get_object(self):

        if 'slug' in self.kwargs:
            slug = escape(self.kwargs.get('slug'))
            return get_object_or_404(Book, slug=slug)


class BookListView(TemplateView):
    """ Displays the book list in a condensed table. """
    template_name = "books/lists.html"

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['to_read'] = get_object_or_404(ItemList, slug="to-read")
        context['now_reading'] = get_object_or_404(ItemList, slug="now-reading")
        context['have_read'] = get_object_or_404(ItemList, slug="have-read")
        context['favorites'] = get_object_or_404(ItemList, slug="favorites")
        return context


class HighlightListView(ListView):

    model = Passage

    template_name = 'books/passage_list.html'

    def get_context_data(self, **kwargs):
        context = super(HighlightListView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.query = None
        self.form = PassageForm()

        passages = Passage.objects.top_rated()
        page = request.GET.get('page')
        self.object_list = self.paginate(passages, page)

        context = self.get_context_data(object_list=self.object_list, query=self.query, form=self.form)

        return self.render_to_response(context)

    def paginate(self, all_passages, page):
        paginator = Paginator(all_passages, 40)

        try:
            passages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            passages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            passages = paginator.page(paginator.num_pages)

        return passages


class SearchHighlightListView(HighlightListView):

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            self.query = escape(request.GET['q'])
            search_results = Passage.search(self.query)
            page = request.GET.get('page')
            self.object_list = self.paginate(search_results, page)
        else:
            self.object_list = []

        context = self.get_context_data(object_list=self.object_list, query=self.query)

        return self.render_to_response(context)


class RandomHighlightView(DetailView):

    model = Passage
    template_name = 'books/passage_random.html'
    context_object_name = 'passage'

    def get_object(self):
        object = Passage.objects.random().get()
        return object


class CreateHighlight(CreateView):
    form_class = PassageForm
    template_name = 'books/passage_create.html'
    success_url = reverse_lazy('books.highlight.list')


class ProtectedView(TemplateView):
    template_name = 'secret.html'

    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class ChapterListView(ListView):
    model = Chapter
    template_name = 'books/table_of_contents.html'


class ChapterView(DetailView):
    model = Chapter
    template_name = 'books/chapter.html'
    context_object_name = 'chapter'

@login_required
def like_highlight(request, pk):
    """ Move the item up one position in the list. """
    passage = get_object_or_404(Passage, pk=pk)
    passage.like()
    return redirect(request.META.get('HTTP_REFERER', None))
