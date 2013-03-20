from lists.models import *
from django.contrib import admin

class ItemInline(admin.TabularInline):
    model = Item

class ItemListAdmin(admin.ModelAdmin):
    ordering = ['created_at']

    inlines = [ItemInline]

    prepopulated_fields = {'slug': ('name',)}
    
    extra = 1

admin.site.register(ItemList, ItemListAdmin)
