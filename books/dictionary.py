import json
from nltk.corpus import wordnet


def lookup(word):
    results = wordnet.synsets(word)
    definitions = []
    for d in results:
        definitions.append(Definition(word, d))
    return definitions


class Definition():
    def __init__(self, word, synset):
        self.word = word
        self.name = synset.name
        self.lexical_type = synset.lexname
        self.lemmas = synset.lemmas
        self.text = synset.definition
        #self.examples = synset.examples

    class Meta:
        fields = ('name', 'text',)
