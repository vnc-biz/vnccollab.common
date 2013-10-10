from plone import api


SEARCH_KEYS = ['user', 'type']


TYPES_NORM = {
    'news'   : ['News Item'],
    'image'  : ['Image'],
    'cast'   : ['Cast Update', 'Cast', 'Cast Comment', 'CastsContainer'],
    'topic'  : ['Cast Update', 'Cast', 'Cast Comment', 'CastsContainer'],
    'link'   : ['Link'],
    'file'   : ['File'],
    'folder' : ['Folder'],
    'document' : ['Document'],
    'event'  : ['Event'],
}


def _key_and_val_from_searchable_text(searchable_text):
    '''Returns the key and arguments from a keyword query'''
    if ':' not in searchable_text:
        return None, None

    parts = searchable_text.split(':')
    key = parts[0].strip()
    val = parts[1].strip()
    return key, val


def _types_from_type_string(type_string):
    '''Returns a list of plone types given a string with types.
    The types in the string are more agreable to be typed by humans
    (like 'news' instead of 'News Items').'''
    parts = type_string.lower().split()
    types = [x for part in parts for x in TYPES_NORM.get(part, [])]
    return types


def _user_ids_from_users_string(user_string):
    '''Returns a list of plone user ids given a string with
    a list of parts of names, surnames or mails.'''
    user_ids = []
    parts = user_string.strip().split()
    for part in parts:
        for id in _user_ids_from_string(part):
            if id and id not in user_ids:
                user_ids.append(id)
    return user_ids


def _user_ids_from_string(str):
    '''Returns a list of plone user ids given a string with
    part of a name, surname or mail.'''
    mdata = api.portal.get_tool(name='portal_memberdata')
    info = mdata.searchMemberData('fullname', str)
    info = info + mdata.searchMemberData('email', str)
    user_ids = [x.get('username', '') for x in info]
    return user_ids


def _is_keyword_search(searchable_text, allowed_keys=None):
    '''True if this search uses keywords.'''
    keys = SEARCH_KEYS

    if allowed_keys is not None:
        keys = [k for k in keys if k in allowed_keys]

    text = ''.join(searchable_text.split())
    is_it = any((text.startswith(key + ':') for key in keys))
    return is_it
