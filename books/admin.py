from django.contrib import admin
from .models import Author, Book, Passage, Chapter, Paragraph
from lists.models import ItemList


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)

    ordering = ['last_name', 'first_name']

    search_fields = ['last_name', 'first_name']

    # automatically generate URL slug from product name
    prepopulated_fields = {'slug': ('first_name', 'last_name',)}


class PassagesInline(admin.TabularInline):
    model = Passage


def add_to_to_read_list(modeladmin, request, queryset):
    add_to_list(queryset, "to-read")


add_to_to_read_list.short_description = "Add to the to-read list"


def add_to_have_read_list(modeladmin, request, queryset):
    add_to_list(queryset, "have-read")


add_to_have_read_list.short_description = "Add to the have-read list"


def add_to_favorites_list(modeladmin, request, queryset):
    add_to_list(queryset, "favorites")


add_to_favorites_list.short_description = "Add to the favorites list"


def add_to_now_reading_list(modeladmin, request, queryset):
    add_to_list(queryset, "now-reading")


add_to_now_reading_list.short_description = "Add to the now-reading list"


def add_to_list(queryset, slug):
    book_list = ItemList.objects.get(slug=slug)
    for book in queryset.order_by("-created_at"):
        book_list.items.create(content_object=book)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)

    inlines = [PassagesInline]

    ordering = ['title']

    search_fields = ['title', 'author']

    # automatically generate URL slug from product name
    prepopulated_fields = {'slug': ('title',)}

    actions = [add_to_have_read_list, add_to_favorites_list, add_to_to_read_list, add_to_now_reading_list]


class PassageAdmin(admin.ModelAdmin):
    list_display = ('book', 'location', 'created_at',)

    search_fields = ['book__title', 'text']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(Chapter)
admin.site.register(Paragraph)
