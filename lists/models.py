from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class ItemList(models.Model):
    """ Represents an ordered list of model objects """
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique URL created for each book list.')
    created_at = models.DateTimeField(default=None)
    
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super(ItemList, self).save(*args, **kwargs)

    def next_position(self):
        results = self.items.all().aggregate(Max('position'))
        curmax = results.get('position__max', 0)
        if curmax is None:     
            return 1
        else:
            return curmax + 1
 
    def __unicode__(self):
        return self.name


class Item(models.Model):
    """ A model object that exists within an ItemList. """
    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content_type'),
            related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    item_list = models.ForeignKey(ItemList, related_name="items")
    position = models.IntegerField(default=None, blank=True)
    created_at = models.DateTimeField(default=None, blank=True)

    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()

        if self.position is None:
            self.position = self.item_list.next_position()

        super(Item, self).save(*args, **kwargs)

    def delete (self):
        items_below = self.item_list.items.filter(position__gt=self.position)
        items_below.update(position = models.F('position') - 1)
        super(Item, self).delete()

    @transaction.commit_on_success 
    def move_to_position(self, new_position):
        """ Move an item to the given position.  Updates the position of
            other items in the list affected by the move.  Raises an
            IndexError if position is outside the list boundary.  
        """
        max_position = self.item_list.items.count()
        in_range = new_position >= 1 and new_position <= max_position
        if in_range:
            current = self.position
            queryset = self.item_list.items.exclude(pk=self.pk)
            if new_position > current:
                queryset = queryset.filter(position__gt=current,
                                           position__lte=new_position)
                queryset.update(position = models.F('position') - 1)
            else:
                queryset = queryset.filter(position__lt=current,
                                           position__gte=new_position)
                queryset.update(position = models.F('position') + 1)

            self.position = new_position
            self.save()
        else:
            raise IndexError("Position is out of range.")

    def move_up(self):
        """ Move this item up one position in the list. """
        self.move_to_position(self.position - 1)

    def move_down(self):
        """ Move this item down one position in the list. """
        self.move_to_position(self.position + 1)

    @models.permalink
    def get_move_up_url(self):
        return ('move_item_up', (), {'id': self.id})

    @models.permalink
    def get_move_down_url(self):
        return ('move_item_down', (), {'id': self.id})

    def __unicode__(self):
        return str(self.content_object) 
