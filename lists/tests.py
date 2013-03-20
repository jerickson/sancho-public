"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from lists.models import ItemList
from books.models import Author


class ItemListPositionTests(TestCase):
    def setUp(self):
        self.list = ItemList.objects.create(name="Favorites", slug="favorites")
        self.list.save()

        tolstoy = Author.objects.create(first_name="Leo", last_name="Tolstoy", slug="leo-tolstoy")
        faulkner = Author.objects.create(first_name="William", last_name="Faulkner", slug="william-faulkner")
        chekhov = Author.objects.create(first_name="Anton", last_name="Chekhov", slug="anton-chekhov")

        self.list.items.create(content_object=tolstoy)
        self.list.items.create(content_object=faulkner)
        self.list.items.create(content_object=chekhov)

    def test_first_position(self):
        self.assertEqual("leo-tolstoy", self.get_author(1).slug)

    def test_second_position(self):
        self.assertEqual("william-faulkner", self.get_author(2).slug)

    def test_third_position(self):
        self.assertEqual("anton-chekhov", self.get_author(3).slug)

    def test_move_to_higher_position(self):
        last_item = self.get_position(3)
        last_item.move_to_position(1)
       
        self.reload_list()
        
        self.assertEqual("anton-chekhov", self.get_author(1).slug)
        self.assertEqual("leo-tolstoy", self.get_author(2).slug)
        self.assertEqual("william-faulkner", self.get_author(3).slug)
         
    def test_move_to_lower_position(self):
        last_item = self.get_position(1)
        last_item.move_to_position(2)
       
        self.reload_list()
        
        self.assertEqual("william-faulkner", self.get_author(1).slug)
        self.assertEqual("leo-tolstoy", self.get_author(2).slug)
        self.assertEqual("anton-chekhov", self.get_author(3).slug)
         
    def test_attempt_move_to_zero_raises_error(self):
        last_item = self.get_position(1)
        self.assertRaises(IndexError, last_item.move_to_position, 0)
    
    def test_move_past_end_of_list_raises_error(self):
        last_item = self.get_position(2)
        self.assertRaises(IndexError, last_item.move_to_position, 4)
    
    def reload_list(self):
        self.list = ItemList.objects.get(id=self.list.id) 
    
    def get_author(self, position):
        return self.get_position(position).content_object    
     
    def get_position(self, position):
        return self.list.items.get(position=position)
