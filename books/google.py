import requests
import json


class GoogleBookQuery():

    # Base address for the Google Api call that queries book info (volumes)
    BASE_URI = "https://www.googleapis.com/books/v1/volumes/?"

    ACCEPTED_PARAMS = ["isbn", "intitle"]

    def __init__(self, query):
        self.query = query

    @staticmethod
    def by_isbn(isbn):
        return GoogleBookQuery({'isbn': isbn})

    def get_first_result(self):
        result = None
        uri = self.build_query_uri()
        r = requests.get(uri)
        result_count = r.json.get("totalItems", 0)

        if result_count > 0:
            items = r.json.get("items")
            first_book_uri = items[0].get("selfLink", "")
            r = requests.get(first_book_uri)
            result = r

        return result

    def get_result(self):
        result = self.get_first_result()
        if result:
            return result.text
        else:
            return result

    def build_query_uri(self):
        query_string = "q="
        for key in self.ACCEPTED_PARAMS:
            if key in self.query:
                param = self.build_param_string(key)
                if param:
                    query_string += param
                    break
        print self.BASE_URI + query_string
        return self.BASE_URI + query_string

    def build_param_string(self, key):
        param = None
        v = self.query[key]
        has_value = v is not None and len(v) > 0
        if has_value:
            words = v.lower().split(" ")
            words.insert(0, key)
            param = ":".join(words)
        return param


class GoogleBook():

    def __init__(self, text):
        self.data = json.loads(text)

    def title(self):
        return self._volume_info()['title']

    def author_fname(self):
        return self.author().split()[0]

    def author_lname(self):
        return self.author().split()[1]

    def author(self):
        return self._volume_info()['authors'][0]

    def description(self):
        return self._volume_info()['description']

    def info_link(self):
        return self._volume_info()['infoLink']

    def thumbnail(self):
        return self._image_links()['thumbnail']

    def small_thumbnail(self):
        return self._image_links()['smallThumbnail']

    def _image_links(self):
        try:
            return self._volume_info()['imageLinks']
        except KeyError:
            return None

    def _volume_info(self):
        try:
            return self.data['volumeInfo']
        except KeyError:
            return None
