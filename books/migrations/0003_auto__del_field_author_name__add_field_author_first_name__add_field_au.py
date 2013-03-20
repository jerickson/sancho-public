# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Author.name'
        db.delete_column('books_author', 'name')

        # Adding field 'Author.first_name'
        db.add_column('books_author', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=200),
                      keep_default=False)

        # Adding field 'Author.last_name'
        db.add_column('books_author', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='test', unique=True, max_length=200),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Author.name'
        raise RuntimeError("Cannot reverse this migration. 'Author.name' and its values cannot be restored.")
        # Deleting field 'Author.first_name'
        db.delete_column('books_author', 'first_name')

        # Deleting field 'Author.last_name'
        db.delete_column('books_author', 'last_name')


    models = {
        'books.author': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Author'},
            'first_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'books.book': {
            'Meta': {'ordering': "['title']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'books.passage': {
            'Meta': {'object_name': 'Passage'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Book']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['books']