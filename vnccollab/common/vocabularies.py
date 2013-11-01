from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class SimpleVocabularyFactory:
    implements(IVocabularyFactory)

    def __init__(self, lst):
        self.lst = lst

    def __call__(self, context):
        terms = [SimpleTerm(value=x[0], token=x[0], title=x[1]) for x in self.lst]
        vocabulary = SimpleVocabulary(terms)
        return vocabulary
