**********************
collective.syndication
**********************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

``collective.syndication`` improves standard syndication on Plone sites by
providing 5 feed types: `Atom`_, iTunes, `NewsML 1`_, `RSS 1.0`_ and `RSS
2.0`_.

This package is a backport for Plone 4.0, 4.1 and 4.2 of `Nathan Van Gheem`_'s
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

NewsML 1
^^^^^^^^

NewsML 1 is an XML standard designed to provide a media-independent,
structural framework for multi-media news.

In this package, we implement part of the standard, to be usable by MSN.
There's no online reference on how MSN expects data, just a PDF included
in the docs folder of this package.

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

.. _`Atom`: https://www.ietf.org/rfc/rfc4287.txt
.. _`NewsML 1`: https://www.iptc.org/site/News_Exchange_Formats/NewsML_1/
.. _`RSS 1.0`: http://web.resource.org/rss/1.0/spec
.. _`RSS 2.0`: https://cyber.law.harvard.edu/rss/rss.html
.. _`Nathan Van Gheem`: https://github.com/vangheem
.. _`Improved Syndication`: https://dev.plone.org/ticket/12908
.. _`advantages`: http://www.intertwingly.net/wiki/pie/Rss20AndAtom10Compared
.. _`opening a support ticket`: https://github.com/collective/collective.syndication/issues
