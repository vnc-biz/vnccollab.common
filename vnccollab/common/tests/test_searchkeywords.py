import unittest2 as unittest

from plone import api

from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME

from vnccollab.common.testing import VNCCOLLAB_COMMON_INTEGRATION_TESTING


class TestSearchKeywords(unittest.TestCase):
    """Test search keywords in cloudstream.

    Currently, there are defined the following keywords:

        user:
        type:

    It returns only entries for the given users.
    """

    layer = VNCCOLLAB_COMMON_INTEGRATION_TESTING

    USER1_ID = 'chuck'
    USER1_MAIL = 'chuck@norris.org'
    USER2_ID = 'jackie'
    USER2_MAIL = 'jackie@chang.org'

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.portal_properties.site_properties.use_email_as_login = True
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        api.user.create(username=self.USER1_ID,
                        email=self.USER1_MAIL,
                        password='secret',
                        roles=['Manager'])

        login(self.portal, self.USER1_MAIL)
        self.portal.invokeFactory(id='folder', type_name='Folder')
        self.folder = self.portal['folder']

        self.folder.invokeFactory('Document', 'doc')
        self.folder.invokeFactory('Event', 'event')

        api.user.create(username=self.USER2_ID,
                        email=self.USER2_MAIL,
                        password='secret',
                        roles=['Manager'])
        login(self.portal, self.USER2_MAIL)
        self.folder.invokeFactory('Document', 'doc2')

    def test_search_one_user(self):
        """Only return entries of one especific user."""
        search = self.portal.restrictedTraverse('@@search')
        query = dict(SearchableText='user: ' + self.USER1_ID)
        results = search.results(query=query)
        results = [x for x in search.results(query=query)]

        # only two entries created by the default user
        assert (len(results) == 2)

        # Only one different user in this search
        #creators = set([x.creator['uid'] for x in entries])
        #assert (len(creators) == 1)
        #assert self.USER1_MAIL in creators
'''
    def test_search_inexistent_user(self):
        """Search for inexisten user."""
        search = self.folder.restrictedTraverse('@@search')
        search.searchable_text = 'user: InexistentUser'
        item_info = search.getItemInfo()

        # No entries
        entries = item_info['entries']
        assert (len(entries) == 0)

    def test_search_several_user(self):
        """Return entries of several user."""
        search = self.folder.restrictedTraverse('@@search')
        search.searchable_text = 'user: {0} {1}'.format(
            self.USER1_ID, self.USER2_ID)
        item_info = search.getItemInfo()

        entries = item_info['entries']
        assert (len(entries) == 3)

        # Two different user in this search
        creators = set([x.creator['uid'] for x in entries])
        assert (len(creators) == 2)
        assert self.USER1_MAIL in creators
        assert self.USER2_MAIL in creators
'''
