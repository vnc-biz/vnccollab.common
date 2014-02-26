from plone import api
from plone.memoize import ram

from vnccollab.common.cache import TimeCacheKey
from vnccollab.common import searchutil


CACHE_TIME = 15 * 60  # 15 minutes


cache = TimeCacheKey(CACHE_TIME)


def get_query(query):
    searchable_text = query.get('SearchableText', '')
    key, val = searchutil._key_and_val_from_searchable_text(searchable_text)
    if key is None or key not in searchutil.SEARCH_KEYS:
        return query

    portal_type = query.get('portal_type', [])

    if key == 'type':
        types = searchutil._types_from_type_string(val)
        portal_type = [x for x in portal_type if x in types]
        query['portal_type'] = portal_type
        del(query['SearchableText'])

    elif key == 'user':
        user_ids = searchutil._user_ids_from_users_string(val)
        query['Creator'] = user_ids
        del(query['SearchableText'])

    return query


def query(params):
    params = get_query(params)
    result = _query(**params)
    return result


@ram.cache(cache)
def _query(**params):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog(**params)
    return result

