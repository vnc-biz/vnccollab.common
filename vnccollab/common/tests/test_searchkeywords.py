import unittest2 as unittest

from zope.publisher.browser import TestRequest

from plone import api
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME

from vnccollab.common.browser.search import Search
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

        self.folder.invokeFactory('Document', 'doc', title='doc1')
        self.folder.invokeFactory('Event', 'event')

        api.user.create(username=self.USER2_ID,
                        email=self.USER2_MAIL,
                        password='secret',
                        roles=['Manager'])
        login(self.portal, self.USER2_MAIL)
        self.folder.invokeFactory('Document', 'doc2', title='doc2')

    def test_search_one_user(self):
        """Only return entries of one especific user."""
        request = TestRequest(form=dict(SearchableText='user: '
                                        + self.USER1_ID))
        view = Search(self.portal, request)
        results = view.results()
        results = [x for x in results]

        # only three results created by the default user, plus the folder
        assert (len(results) == 3)

    def test_search_type(self):
        """Only return entries of especific type."""
        request = TestRequest(form=dict(SearchableText='type:Document'))
        view = Search(self.portal, request)
        results = view.results()
        results = [x for x in results]

        self.assertTrue(len(results) == 2)
        for r in results:
            self.assertIn(r.Title(), ('doc1', 'doc2'))
