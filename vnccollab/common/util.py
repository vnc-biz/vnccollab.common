from zope.component import getUtility, getMultiAdapter

from plone import api
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletAssignmentMapping


MANAGER_NAMES = ['plone.leftcolumn', 'plone.rightcolumn',
                 'plone.dashboard1', 'plone.dashboard2',
                 'plone.dashboard3', 'plone.dashboard4']


def replace_all_portlets(fn):
    '''Replace instances of portlets with the result of fn.

    fn takes a portlet and its name and returns None or a new portlet.
    If it returns None, nithing is changed. If it returns a portlet, the
    old one is replaced with the new one.
    '''
    replace_all_general_portlets(fn)
    replace_all_content_portlets(fn)


def replace_all_general_portlets(fn):
    '''Replace portlets for the portal.'''
    portal = api.portal.get()
    managers = get_managers(portal)

    for manager in managers:
        for cat_name, category in manager.items():
            for map_name, mapping in category.items():
                for portlet_name, portlet in mapping.items():
                    new_portlet = fn(portlet, portlet_name)
                    if new_portlet is not None:
                        mapping._data[portlet_name] = new_portlet


def replace_all_content_portlets(fn):
    '''Replace portlets in content objects.'''
    all_content = all_content_with_portlets()
    for content in all_content:
        managers = get_managers(content)
        for manager in managers:
            mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)
            for portlet_name, portlet in mapping.items():
                new_portlet = fn(portlet, portlet_name)
                if new_portlet is not None:
                    mapping._data[portlet_name] = new_portlet


def _class_name(obj):
    '''Returns the full qualified class name of an object.'''
    return '{0}.{1}'.format(obj.__module__, obj.__class__.__name__)


def all_content_with_portlets():
    '''Returns all the content objects that have a portlet assigned.'''
    portal = api.portal.get()
    catalog = api.portal.get_tool(name='portal_catalog')

    all_brains = catalog(show_inactive=True, language="ALL",
                         object_provides=ILocalPortletAssignable.__identifier__)
    all_content = [brain.getObject() for brain in all_brains]
    all_content = list(all_content) + [portal]
    return all_content


def mapping_from_manager(manager, content):
    '''Returns the mappings associated to a portelt manager.'''
    mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)
    items = mapping.items()
    return items

def get_managers(content):
    '''Returns the portlet managers.'''
    managers = [getUtility(IPortletManager, name=manager_name, context=content)
                    for manager_name in MANAGER_NAMES]
    return managers
