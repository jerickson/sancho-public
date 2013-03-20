"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from datetime import datetime

from books.models import Clip


class ClipParserTest(TestCase):

    def setUp(self):
        lines = []
        lines.append("Moby Dick (Herman Mellville)")
        lines.append("- Highlight on Page 1 | Loc. 0-20 | Added on Sunday, September 23, 2012, 02:58 PM")
        lines.append("")
        lines.append("Call me Ishmael.")
        self.clip = Clip(lines)

    def test_parse_title(self):
        self.assertEqual("Moby Dick", self.clip.title)

    def test_parse_author(self):
        self.assertEqual("Herman Mellville", self.clip.author)

    def test_parse_location(self):
        self.assertEqual("Page 1 - Loc. 0-20", self.clip.location)

    def test_parse_added_on(self):
        self.assertEqual(datetime(2012, 9, 23, 14, 58, 0), self.clip.added_on)

    def test_parse_clip_text(self):
        self.assertEqual("Call me Ishmael.", self.clip.clip)

    def test_parse_author_first_name(self):
        self.assertEqual("Herman", self.clip.author_first_name())

    def test_parse_author_first_name(self):
        self.assertEqual("Mellville", self.clip.author_last_name())


class ParseUnusualClipTest(TestCase):

    def setUp(self):
        lines = []
        lines.append("The Great Gatsby (F. Scott Fitzgerald)")
        lines.append("- Highlight Loc. 0-20 | Added on Sunday, September 23, 2012, 02:58 PM")
        lines.append("")
        lines.append("In my younger and more vulnerable years my father gave me some advice...")
        self.clip = Clip(lines)

    def test_parse_author_first_name(self):
        self.assertEqual("F. Scott", self.clip.author_first_name())

    def test_parse_author_last_name(self):
        self.assertEqual("Fitzgerald", self.clip.author_last_name())

    def test_parse_location(self):
        self.assertEqual("Loc. 0-20", self.clip.location)


class ParseClipWithMultipleAuthorsTest(TestCase):

    def setUp(self):
        lines = []
        lines.append("War and Peace (Leo Tolstoy, Richard Pevear and Larissa Volokhonsky)")
        lines.append("- Highlight on Page 222 | Loc. 5514-17  | Added on Tuesday, March 15, 2011, 04:08 AM")
        lines.append("")
        lines.append("When an insecure man is silent at first acquaintance and shows an awareness of...")
        self.clip = Clip(lines)

    def test_parse_author_first_name(self):
        self.assertEqual("Leo", self.clip.author_first_name())

    def test_parse_author_last_name(self):
        self.assertEqual("Tolstoy", self.clip.author_last_name())


class ParseClipWithMultipleAuthorsAndSepTest(TestCase):

    def setUp(self):
        lines = []
        lines.append("A Moveable Feast (Ernest Hemingway and Patrick Hemingway)\r\n")
        lines.append("- Highlight on Page 222 | Loc. 5514-17  | Added on Tuesday, March 15, 2011, 04:08 AM")
        lines.append("")
        lines.append("When an insecure man is silent at first acquaintance and shows an awareness of...")
        self.clip = Clip(lines)

    def test_parse_author(self):
        self.assertEqual("Ernest Hemingway", self.clip.author)

    def test_parse_author_first_name(self):
        self.assertEqual("Ernest", self.clip.author_first_name())

    def test_parse_author_last_name(self):
        self.assertEqual("Hemingway", self.clip.author_last_name())
