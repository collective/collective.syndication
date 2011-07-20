README.txt
==========

    >>> portal = layer['portal']
    >>> from Products.CMFPlone.utils import _createObjectByType
    >>> _createObjectByType(type_name="Topic", container=portal, id="atomic", title=u"Atomic Content", description=u"A collection of atomic content.")
    <ATTopic at /plone/atomic>
    >>> atomic = portal['atomic']
    >>> from zope.testbrowser.browser import Browser
    >>> browser = Browser()

Site-wide syndication
=====================
    >>> portal.setTitle(u"Site Root")
    >>> browser.open(portal.absolute_url()+'/atom.xml')
    >>> browser.url
    'http://nohost/plone/atom.xml'
    >>> browser.headers["Content-type"]
    'application/atom+xml;charset=utf-8'
    >>> u'<title>Site Root</title>' in browser.contents
    True

Drop-in replacement for RSS syndication
=======================================
    >>> atomic.absolute_url()
    >>> browser.open(atomic.absolute_url()+'/atom.xml')
    >>> browser.url
    'http://nohost/plone/atomic/atom.xml'
    >>> browser.headers["Content-type"]
    'application/atom+xml;charset=utf-8'
    >>> u'<title>Atomic Content</title>' in browser.contents
    True
