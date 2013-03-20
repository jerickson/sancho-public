

class AmazonClippingsFile():
    """
    Example:

    # Iterate through the clippings in an Amazon kindle clippings file.

    for clip in AmazonClippingsFile("Clippings.txt"):
      print "Processing clip %s (%s)" % (clip.author, clip.added_on)

    """


    LINES_PER_CLIP = 5

    def __init__(self, file_path):
        self.lines = open(file_path, 'r').readlines()
        self.last_line = len(self.lines)
        self.cursor = 0

    def __iter__(self):
        return self

    def next(self):
        if self.cursor < self.last_line:
            clip_lines = self.next_clip_lines()
            self.advance_cursor()
            return Clip(clip_lines)
        else:
            raise StopIteration

    def next_clip_lines(self):
        return self.lines[self.cursor:self.clip_end()]

    def clip_end(self):
        return self.cursor + self.LINES_PER_CLIP

    def advance_cursor(self):
        self.cursor = self.clip_end()


class Clip():

    def __init__(self, lines):
        """ Must strip the input lines otherwise it will mess up """

        lines = self.clean_input(lines)

        self.title = self.parse_title(lines[0])
        self.author = self.parse_author(lines[0])
        self.location = self.parse_location(lines[1])
        self.added_on = self.parse_added_on(lines[1])
        self.clip = lines[3].strip()

    def clean_input(self, lines):
        """
        Strip whitespace characters from the beginning and end of all
        input lines to simplify the string matching algorithms.
        """
        cleaned = []
        for line in lines:
            cleaned.append(line.strip())
        return cleaned

    def author_first_name(self):
        idx = self.author.rfind(' ')
        return self.author[0:idx].strip()

    def author_last_name(self):
        idx = self.author.rfind(' ')
        return self.author[idx:].strip()

    def has_multiple_authors(self):
        return self.author.find(',') or self.author.find('and')

    def parse_title(self, line):
        title = re.search("^(.*)(?=\()", line).group(0)
        return title.strip()

    def parse_author(self, line):
        idx = line.rfind('(')
        author = re.search("\((.+)\)$", line[idx:]).group(0)
        author = author.strip().strip('(').strip(')')
        has_multiple = ("," in author) or ("and" in author)

        if has_multiple:
            author = self.parse_first_author(author)

        return author

    def parse_first_author(self, author):
        if "," in author:
            idx = author.index(",")
            return author[0:idx].strip()

        if "and" in author:
            idx = author.index("and")
            return author[0:idx].strip()

    def parse_location(self, line):
        line = line.replace("- Highlight ", "")
        line = line.replace("on ", "")
        last_pipe = line.rfind('|')
        return "-".join(line[:last_pipe].split('|')).strip()

    def parse_added_on(self, line):
        fields = line.split('|')
        last = len(fields) - 1
        added = fields[last].strip()
        return datetime.strptime(added, "Added on %A, %B %d, %Y, %I:%M %p")

    def __unicode__(self):
        return "%s : %s : %s : %s" % (self.title,
                                      self.author,
                                      self.location,
                                      self.added_on)
