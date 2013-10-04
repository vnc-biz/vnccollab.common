from plone import api
from plone.app.search.browser import Search as OriginalSearch
from plone.app.contentlisting.interfaces import IContentListing
from Products.ZCTextIndex.ParseTree import ParseError
from Products.CMFPlone.PloneBatch import Batch

from vnccollab.common import searchutil


class Search(OriginalSearch):
    '''Search extension to allow keyword searchs'''

    def results(self, query=None, batch=True, b_size=10, b_start=0,
                allowed_keys=None):
        ''' Get properly wrapped search results from the catalog.
        Everything in Plone that performs searches should go through this
        view.
        'query' should be a dictionary of catalog parameters.
        '''
        searchable_text = self.get_searchable_text(query)
        if searchutil._is_keyword_search(searchable_text, allowed_keys):
            results = self.keyword_results(query, batch, b_size, b_start)
            return results

        else:
            return OriginalSearch.results(self, query, batch, b_size, b_start)

    def get_searchable_text(self, query=None):
        '''Returns the searchable text for the query.'''
        if query is None:
            query = {}
        request = self.request
        text = query.get('SearchableText', '')
        if not text:
            text = request.form.get('SearchableText', '')
        if not text:
            # Without text, the only meaningful case is Subject
            text = request.form.get('Subject', '')
        return text

    def keyword_results(self, query=None, batch=True, b_size=10, b_start=0):
        '''Returns the result of a keywor query.
        The current accepted keywords are:
            user: An ORed list of words that should appear in the user info.
            type: An ORed list of content types.
        '''
        searchable_text = self.get_searchable_text(query)
        key, val = searchutil._key_and_val_from_searchable_text(searchable_text)
        if key == 'type':
            return self.type_results(query, batch, b_size, b_start, val)
        elif key == 'user':
            return self.user_results(query, batch, b_size, b_start, val)
        else:
            return []

    def type_results(self, query=None, batch=True, b_size=10, b_start=0, type_string=''):
        '''Returns the result of a search for the given content types.
        '''
        query = self._prepare_query(query, batch, b_size, b_start)
        types = searchutil._types_from_type_string(type_string)
        portal_type = [x for x in query.get('portal_type', []) if x in types]
        query['portal_type'] = portal_type
        del(query['SearchableText'])
        results = self._result_from_query(query, batch, b_size, b_start)
        return results

    def user_results(self, query=None, batch=True, b_size=10, b_start=0, users_string=''):
        '''Returns the result of a search for the user which info coincides with args.
        '''
        query = self._prepare_query(query, batch, b_size, b_start)
        user_ids = searchutil._user_ids_from_users_string(users_string)
        query['Creator'] = user_ids
        del(query['SearchableText'])
        results = self._result_from_query(query, batch, b_size, b_start)
        return results

    def _prepare_query(self, query=None, batch=True, b_size=10, b_start=0):
        '''Converts the query in a dict, obtaining info from the request, if not
        directly available.'''
        if query is None:
            query = {}
        if batch:
            query['b_start'] = b_start = int(b_start)
            query['b_size'] = b_size
        query = self.filter_query(query)
        return query

    def _result_from_query(self, query=None, batch=True, b_size=10, b_start=0):
        '''Given a query (as dict or None) returns its result.'''
        if query is None:
            results = []

        else:
            catalog = api.portal.get_tool(name='portal_catalog')
            try:
                results = catalog(**query)
            except ParseError:
                return []

        results = IContentListing(results)
        if batch:
            results = Batch(results, b_size, b_start)
        return results
