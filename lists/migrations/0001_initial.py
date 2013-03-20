# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemList'
        db.create_table('lists_itemlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=None)),
        ))
        db.send_create_signal('lists', ['ItemList'])

        # Adding model 'Item'
        db.create_table('lists_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_item', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.TextField')()),
            ('item_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['lists.ItemList'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=None)),
        ))
        db.send_create_signal('lists', ['Item'])


    def backwards(self, orm):
        # Deleting model 'ItemList'
        db.delete_table('lists_itemlist')

        # Deleting model 'Item'
        db.delete_table('lists_item')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lists.item': {
            'Meta': {'ordering': "['position']", 'object_name': 'Item'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_item'", 'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['lists.ItemList']"}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        'lists.itemlist': {
            'Meta': {'object_name': 'ItemList'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['lists']