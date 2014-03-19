from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

from vnccollab.common.livesearch import query, get_query, _query
from vnccollab.common.tests.base import IntegrationTestCase


class TestLivesearch(IntegrationTestCase):
    members = (
        ('secret', 'Scott Tiger', 'scott@tiger.com',
            ['Manager'], '2013-09-24'),
        ('secret', 'Johann Sebastian Bach', 'johan@bach.com',
            ['Manager'], '2013-09-24'),)

    def setUp(self):
        super(TestLivesearch, self).setUp()
        self.populateSite()

    def populateSite(self):
        self.setRoles(['Manager'])
        if 'Members' in self.portal:
            self.portal._delObject('Members')
            self.folder = None
        if 'news' in self.portal:
            self.portal._delObject('news')
        if 'events' in self.portal:
            self.portal._delObject('events')
        if 'front-page' in self.portal:
            self.portal._delObject('front-page')
        self.portal.invokeFactory('Document', 'doc1 foo', title='doc1 foo')
        self.portal.invokeFactory('Document', 'doc2 foo', title='doc2 foo')
        self.portal.invokeFactory('Document', 'doc3 foo', title='doc3 foo')
        self.portal.invokeFactory('Folder', 'folder1')
        self.portal.invokeFactory('Link', 'link1')
        self.portal.link1.setRemoteUrl('http://plone.org')
        self.portal.link1.reindexObject()
        folder1 = getattr(self.portal, 'folder1')
        self._login('johan@bach.com')
        folder1.invokeFactory('Document', 'doc11', title='doc11 foo')
        folder1.invokeFactory('Document', 'doc12', title='doc12 foo')
        folder1.invokeFactory('Document', 'doc13', title='doc13 foo')
        self.portal.invokeFactory('Folder', 'folder2')
        folder2 = getattr(self.portal, 'folder2')
        self._login('scott@tiger.com')
        folder2.invokeFactory('Document', 'doc21', title='doc21 foo')
        folder2.invokeFactory('Document', 'doc22', title='doc22 foo')
        folder2.invokeFactory('Document', 'doc23', title='doc23 foo')
        folder2.invokeFactory('File', 'file21')
        folder2.invokeFactory('Folder', 'folder21')
        self.setRoles(['Member'])

    def test_query(self):
        ploneUtils = getToolByName(self.portal, 'plone_utils')

        params = {'SearchableText': 'foo',
                  'portal_type': ploneUtils.getUserFriendlyTypes(),
                  'sort_limit': 2}
        results = query(params)
        self.assertTrue(len(results) == 2)
        for r in results:
            self.assertIn(r.getObject().Title(),
                ('doc3 foo', 'doc2 foo', 'doc1 foo'))

        params = {'SearchableText': 'type:Document',
                  'portal_type': ploneUtils.getUserFriendlyTypes(),
                 }
        results = query(params)
        self.assertTrue(len(results) == 9)
        for r in results:
            self.assertEqual(r.portal_type, 'Document')

        params = {'SearchableText': 'user:johan@bach.com',
                  'portal_type': ploneUtils.getUserFriendlyTypes(),
                 }
        results = query(params)
        self.assertTrue(len(results) == 4)
        for r in results:
            self.assertEqual(results[0].getObject().Creator(), 'johan@bach.com')
