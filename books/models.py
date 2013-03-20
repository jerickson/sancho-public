from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, F
from django.template.defaultfilters import slugify
from django.utils import timezone
from datetime import datetime
import json
import re

from .managers import HighlightManager
from .google import GoogleBookQuery, GoogleBook


class Author(models.Model):
    """ The authors, who write the books. """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,
                            help_text='Unique URL created for each author.')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super(Author, self).save(*args, **kwargs)

    class Meta:
        ordering = ['last_name', 'first_name']

    @models.permalink
    def get_absolute_url(self):
        return ('books.views.author.show', (), {'author_slug': self.slug})

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Book(models.Model):
    """ The books I read. """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique URL created for each book.')
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    extra = models.TextField(null=True, blank=True, help_text='Google Books API query results for the book (JSON)')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Save this book. """
        if self.created_at is None:
            self.created_at = timezone.now()

        if self.slug == '':
            self.slug = slugify(self.title)

        super(Book, self).save(*args, **kwargs)

    def recent_highlight(self):
        """ Return the most recent highlight for this book. """
        if self.passage_set.all().count() == 0:
            return None
        return self.passage_set.all()[0]

    def google(self):
        if not self.extra:
            if self.isbn13:
                query = GoogleBookQuery.by_isbn(self.isbn13)
                self.extra = query.get_result()
                self.save()

        if self.extra:
            return GoogleBook(self.extra)
        else:
            return None

    def _query_google_book(self):
        query = GoogleBookQuery.by_isbn(self.isbn13)
        self.extra = query.get_result()

    class Meta:
        ordering = ['title']

    @models.permalink
    def get_absolute_url(self):
        return ('books.views.book.show', (), {'book_slug': self.slug})

    def __unicode__(self):
        return self.title

    @staticmethod
    def create_by_isbn13(isbn):
        query = GoogleBookQuery.by_isbn(isbn)
        json = query.get_result()
        gbook = GoogleBook(json)
        book = Book(title=gbook.title(), isbn13=isbn)
        author, result = Author.objects.get_or_create(
                            first_name=gbook.author_fname(),
                            last_name=gbook.author_lname())
        book.author = author
        book.extra = json
        book.save()
        return book


class Passage(models.Model):
    """ A passage from a book or short story. """
    MANUAL_ENTRY = 1
    KINDLE_CLIP = 2

    SOURCES = (
        (MANUAL_ENTRY, 'Manual Entry'),
        (KINDLE_CLIP, 'Kindle'),
    )

    book = models.ForeignKey(Book)
    context = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    source = models.IntegerField(choices=SOURCES, default=MANUAL_ENTRY)
    created_at = models.DateTimeField()
    likes = models.IntegerField(default=1)
    last_liked = models.DateTimeField(null=True)

    objects = HighlightManager()

    def save(self, *args, **kwargs):
        """ On save, update timestamps. """
        if self.created_at is None:
            self.created_at = timezone.now()
        if self.last_liked is None:
            self.last_liked = self.created_at

        super(Passage, self).save(*args, **kwargs)

    @staticmethod
    def search(query):
        """ A very simple search for text within a passage. """
        if query:
            return Passage.objects.filter(
                        Q(text__icontains=query) |
                        Q(book__title__icontains=query) |
                        Q(book__author__last_name__icontains=query))
        else:
            return []

    def like(self):
        self.likes = F('likes') + 1
        self.last_liked = timezone.now()
        self.save()

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.text[:50]


class Chapter(models.Model):
    book = models.ForeignKey(Book)
    name = models.CharField(max_length=250)
    position = models.IntegerField(unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ['position']
            
    @models.permalink
    def get_absolute_url(self):
        return ('books.chapter', (), {'slug': self.slug})
    
    def __unicode__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.name)
        super(Chapter, self).save(*args, **kwargs)


class Paragraph(models.Model):
    chapter = models.ForeignKey(Chapter)
    text = models.TextField()
    position = models.IntegerField()
    
    class Meta:
        ordering = ['chapter', 'position']

    def __unicode__(self):
        return "%s" % (self.text[:75])

