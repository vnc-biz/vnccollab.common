from zope.component import getUtility, getMultiAdapter
from Products.Five.browser import BrowserView

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRetriever, IPortletRenderer


class PortletDeferredRendererHelperView(BrowserView):
    ''' '''
    def __call__(self):
        manager_name = self.request.get('manager', None)
        name = self.request.get('name', None)
        key = self.request.get('key', None)

        if not manager_name or not name or not key:
            return ''

        manager = self.get_manager(manager_name)
        if not manager:
            return ''

        assignment = self.get_portlet_assignment(manager, name, key)
        if not assignment:
            return ''

        renderer = self.get_portlet_renderer(manager, assignment)
        if not renderer:
            return ''

        try:
            renderer.deferred_update()
            return renderer.render()
        except:
            return ''

    def get_manager(self, manager_name):
        try:
            manager = getUtility(IPortletManager,
                                 name=manager_name,
                                 context=self.context)
            return manager
        except:
            return None

    def get_portlet_assignment(self, manager, name, key):
        retriever = getMultiAdapter((self.context, manager,), IPortletRetriever)
        if not retriever:
            return None

        for assignment in retriever.getPortlets():
            if assignment['key'] == key and assignment['name'] == name:
                return assignment['assignment']

        return None

    def get_portlet_renderer(self, manager, assignment):
        try:
            renderer = getMultiAdapter((self.context,
                                        self.request,
                                        self, manager,
                                        assignment), IPortletRenderer)
            return renderer
        except:
            return None
