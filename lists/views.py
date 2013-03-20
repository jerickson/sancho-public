from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404
from lists.models import Item


def check_user_allowed(user):
    return user.is_authenticated()


@user_passes_test(check_user_allowed)
def move_item_up(request, id):
    """ Move the item up one position in the list. """
    item = get_object_or_404(Item, pk=id)
    item.move_up()
    return redirect(request.META.get('HTTP_REFERER', None))


@user_passes_test(check_user_allowed)
def move_item_down(request, id):
    """ Move the item down one position in the list. """
    item = get_object_or_404(Item, pk=id)
    item.move_down()
    return redirect(request.META.get('HTTP_REFERER', None))


@user_passes_test(check_user_allowed)
def move_item_to_list(request, id, list_id):
    item = get_object_or_404(Item, pk=id)
    list = get_object_or_404(ItemList, pk=list_id)

    # Add item to the top of the given list
    list.items.create(content_object = item.content_object,
                      position = 1)

    item.delete()
    
