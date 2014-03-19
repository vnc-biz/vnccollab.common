from zope.schema.vocabulary import SimpleTerm

from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

from vnccollab.common.vocabularies import SimpleVocabularyFactory
from vnccollab.common.tests.base import IntegrationTestCase


class TestVocabularies(IntegrationTestCase):
    def test_vocabularies(self):
        v = SimpleVocabularyFactory([['av', 'ak'], ['bv', 'bk']])
        values = v(self.portal)
        for v in values:
            self.assertTrue(isinstance(v, SimpleTerm))
            self.assertIn(v.title, ('ak', 'bk'))
            self.assertIn(v.value, ('av', 'bv'))
