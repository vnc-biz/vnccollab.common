vnccollab.common
================

Overview
--------

vnccollab.common is a support package for vnccollab.* add-ons. It offers the
following features:

* A convenience memoizer class based on last time access.
* Keyword Search.
* Simple Vocabulary Factory.
* A convenience base class for deferred portlets.

TimeCacheKey
------------

TimeCacheKey is a helper class to add volatile cache based on last time access. You can use it in the following way::

    >>> from plone.memoize import ram
    >>> from vnccollab.common.cache import TimeCacheKey
    >>> CACHE_TIME = 15 * 60  # 15 minutes
    >>> cache = TimeCacheKey(CACHE_TIME)
    >>> ram(cache)
    >>> def sum(a, b): return a + b
    ...
    

Keyword Search
--------------

A keyword search is a special kind of search that takes place when a keyword
suffixed by ``:`` is present in the search string. This package offers a 
``search`` view with kwyword search.

Currently, there are two keyword defined:

- ``type:`` keyword: The search returns only object of the types specified
  in the query.
- ``user:```keyword: The search returns only objects created by the user
  specified in the query.

Simple Vocabulary Factory
-------------------------

``SimpleVocabularyFactory`` is a convenience class for the creation of 
vocabularies based in a list of tuples::

    >>> from vnccollab.common.vocabularies import SimpleVocabularyFactory
    >>> semaphore = [('r', 'Red'), ('y', 'Yellow'), ('g', 'Green')]
    >>> semaphoreVocabulary = SimpleVocabularyFactory(semaphore)

Deferred Portlet
----------------

``DeferredRenderer`` is a convenience class for the creation of deferred 
portlets. It extends ``plone.app.portlets.portlets.base.DeferredRendered`` 
and adds easy access to the portlet metadata. This class is intended to 
be used by other vnccollab packages.

