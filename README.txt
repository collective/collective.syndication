**********************
collective.syndication
**********************

Life, the Universe, and Everything
----------------------------------

``collective.syndication`` improves standard syndication on Plone sites by
providing 4 feed types: `RSS 1.0`_, `RSS 2.0`_, `Atom`_ and iTunes.

This package is a backport for Plone 4.1 and 4.2 of `Nathan Van Gheem`_'s
`Improved Syndication`_ PLIP implementation made for Plone 4.3.

Don't Panic
-----------

Atom
^^^^

Atom is an XML-based document format that describes lists of related
information known as "feeds". Feeds are composed of a number of items, known
as "entries", each with an extensible set of attached metadata. For example,
each entry has a title.

The primary use case that Atom addresses is the syndication of Web content
such as weblogs and news headlines to Web sites as well as directly to user
agents.

Atom feeds have multiple `advantages`_ over RSS feeds.

iTunes
^^^^^^

TBD.

NewsML
^^^^^^

TBD.

RSS 1.0 (RDF Site Summary)
^^^^^^^^^^^^^^^^^^^^^^^^^^

RDF Site Summary is a lightweight multipurpose extensible metadata description
and syndication format. RSS is an XML application, conforms to the W3C's RDF
Specification and is extensible via XML-namespace and/or RDF based
modularization.

RSS 2.0
^^^^^^^

TBD.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.syndication.png
    :target: http://travis-ci.org/collective/collective.syndication

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`RSS 1.0`: http://web.resource.org/rss/1.0/spec
.. _`RSS 2.0`: https://cyber.law.harvard.edu/rss/rss.html
.. _`Atom`: https://www.ietf.org/rfc/rfc4287.txt
.. _`Nathan Van Gheem`: https://github.com/vangheem
.. _`Improved Syndication`: https://dev.plone.org/ticket/12908
.. _`advantages`: http://www.intertwingly.net/wiki/pie/Rss20AndAtom10Compared
.. _`opening a support ticket`: https://github.com/collective/collective.syndication/issues
