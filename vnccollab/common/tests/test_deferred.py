from zope.component import getUtility

from plone.app.testing import setRoles
from plone.portlets.manager import PortletManager
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.portlets.news import Assignment
from plone.app.portlets.portlets.news import Renderer

from vnccollab.common.portlets.deferred import DeferredRenderer
from vnccollab.common.browser.deferred import PortletDeferredRendererHelperView
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

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.portal
        request = request or self.app.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = assignment or Assignment()

        return DeferredRenderer(context, request, view, manager, assignment)

    def test_renderer(self):
        renderer = self.renderer(self.portal)
        renderer.update()
        self.assertTrue(renderer.initializing)
        self.assertTrue('manager' in renderer.metadata)
        self.assertTrue('name' in renderer.metadata)
        self.assertTrue('key' in renderer.metadata)
        self.assertEqual(renderer.metadata['manager'], '')
        self.assertEqual(renderer.metadata['name'], '')
        self.assertEqual(renderer.metadata['key'], '')

        renderer.__portlet_metadata__ = {'manager': 'manager', 'name': 'name', 'key': 'key'}
        renderer.update()
        self.assertTrue(renderer.initializing)
        self.assertTrue('manager' in renderer.metadata)
        self.assertTrue('name' in renderer.metadata)
        self.assertTrue('key' in renderer.metadata)
        self.assertEqual(renderer.metadata['manager'], 'manager')
        self.assertEqual(renderer.metadata['name'], 'name')
        self.assertEqual(renderer.metadata['key'], 'key')

        self.assertRaises(TypeError, renderer.deferred_update)

        def refresh(self):
            self.__portlet_metadata__['name'] = 'new name'
        DeferredRenderer.refresh = refresh  # lambda self: self.__portlet_metadata__['name'] = 'new name'

        renderer.deferred_update()
        self.assertFalse(renderer.initializing)
        self.assertTrue('manager' in renderer.metadata)
        self.assertTrue('name' in renderer.metadata)
        self.assertTrue('key' in renderer.metadata)
        self.assertEqual(renderer.metadata['manager'], 'manager')
        self.assertEqual(renderer.metadata['name'], 'new name')
        self.assertEqual(renderer.metadata['key'], 'key')


    def test_PortletDeferredRendererHelperView(self):
        view = PortletDeferredRendererHelperView(self.portal, self.app.REQUEST)
        self.assertTrue(view() == '')

        self.app.REQUEST['manager'] = 'foo bar'
        self.app.REQUEST['name'] = 'foo bar'
        self.app.REQUEST['key'] = 'foo bar'
        view = PortletDeferredRendererHelperView(self.portal, self.app.REQUEST)
        self.assertTrue(view() == '')

        self.app.REQUEST['manager'] = 'plone.dashboard1'
        view = PortletDeferredRendererHelperView(self.portal, self.app.REQUEST)
        self.assertTrue(view() == '')

        self.app.REQUEST['name'] = 'news'
        view = PortletDeferredRendererHelperView(self.portal, self.app.REQUEST)
        self.assertTrue(view() == '')

        self.app.REQUEST['name'] = 'news'
        self.app.REQUEST['key'] = 'scott@tiger.com'
        view = PortletDeferredRendererHelperView(self.portal, self.app.REQUEST)
        self.assertTrue(view() == '')

        manager = view.get_manager('plone.dashboard1')
        self.assertTrue(isinstance(manager, PortletManager))

        assignment = view.get_portlet_assignment(manager, 'news', 'scott@tiger.com')
        self.assertTrue(isinstance(assignment, Assignment))

        renderer = view.get_portlet_renderer(manager, assignment)
        self.assertTrue(isinstance(renderer, Renderer))
