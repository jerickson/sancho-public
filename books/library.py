

class BookParser:

    def __init__(self, path, chapter_tokens):
        self.path = path
        self.chapter_tokens = chapter_tokens
        self.chapters = {}
        self.file = None

    def parse(self):
        chapter = None
        token = self.next_chapter_token()
        for paragraph in self.paragraphs():
            if token:
                new_chapter = paragraph.startswith(token)
                if new_chapter:
                    #print "Found " + token
                    chapter = [] 
                    self.chapters[token] = chapter
                    token = self.next_chapter_token()
            
            if chapter is not None:
                paragraph = paragraph.replace('\n', ' ')
                chapter.append(paragraph)
        
        return self.chapters

    def paragraphs(self, separator=None):
        """
        Builds and returns the list of paragraphs the file.
        """
        file = open(self.path)
        if not callable(separator):
            def separator(line): return line == '\n'
        paragraph = []
        for line in file:
            if separator(line):
                if paragraph:
                    yield ''.join(paragraph)
                    paragraph = []
            else:
                paragraph.append(line)
        yield ''.join(paragraph)
         

    def next_chapter_token(self):
        if len(self.chapter_tokens) > 0:
            return self.chapter_tokens.pop(0)
        else:
            None


def parse():
    chapters = ["ETYMOLOGY.", "EXTRACTS (Supplied by a Sub-Sub-Librarian)."]
    for i in range(1, 135):
        chapters.append("CHAPTER %s." % i)
    chapters.append("Epilogue")

    moby_dick = BookParser("moby.txt", chapters)
    return moby_dick.parse()
