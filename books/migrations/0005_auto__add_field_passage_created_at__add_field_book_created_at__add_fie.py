# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Passage.created_at'
        db.add_column('books_passage', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 6, 8, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Book.created_at'
        db.add_column('books_book', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 6, 8, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Book.updated_at'
        db.add_column('books_book', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 6, 8, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Author.created_at'
        db.add_column('books_author', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 6, 8, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Author.updated_at'
        db.add_column('books_author', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 6, 8, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Passage.created_at'
        db.delete_column('books_passage', 'created_at')

        # Deleting field 'Book.created_at'
        db.delete_column('books_book', 'created_at')

        # Deleting field 'Book.updated_at'
        db.delete_column('books_book', 'updated_at')

        # Deleting field 'Author.created_at'
        db.delete_column('books_author', 'created_at')

        # Deleting field 'Author.updated_at'
        db.delete_column('books_author', 'updated_at')


    models = {
        'books.author': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Author'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'books.book': {
            'Meta': {'ordering': "['title']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Author']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'books.passage': {
            'Meta': {'object_name': 'Passage'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Book']"}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['books']