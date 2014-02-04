There's a frood who really knows where his towel is
---------------------------------------------------

1.0b4 (unreleased)
^^^^^^^^^^^^^^^^^^

- Nothing changed yet.


1.0b3 (2014-02-04)
^^^^^^^^^^^^^^^^^^

- Fix a problem with ViewPageTemplateFile overriding the Content-Type header,
  now we set the header after rendering the body, this way third party products
  can't break the feeds Content-Type. [jpgimenez]


1.0b2 (2014-01-23)
^^^^^^^^^^^^^^^^^^

- Obey limit parameter on feeds (fixes `#17`_). [jpgimenez]

- Fix a typo in URLs pointing to files (closes `#19`_). [jpgimenez]

- Implement rendering of body in Atom feeds (closes `#18`_). [jpgimenez]

- Change 'Render Body' future to render the content-core macro, not just the body field. [jpgimenez]


1.0b1 (2013-09-03)
^^^^^^^^^^^^^^^^^^

- Replace beautifulsoup4 with lxml. [jpgimenez] 
- Fix a bug with body text coming from dexterity content. [jpgimenez] 

1.0a4 (2013-03-27)
^^^^^^^^^^^^^^^^^^

- (Bugfix) Return proper headers with the feeds. [frapell]


1.0a3 (2013-03-21)
^^^^^^^^^^^^^^^^^^

- Don't use an interface as filtering mechanism to get NewsML items. [frapell]


1.0a2 (2013-01-15)
^^^^^^^^^^^^^^^^^^

- Implement NewsML 1 syndication. [frapell]


1.0a1 (2013-01-10)
^^^^^^^^^^^^^^^^^^

- Initial release.

.. _`#17`: https://github.com/collective/collective.syndication/issues/17
.. _`#18`: https://github.com/collective/collective.syndication/issues/18
.. _`#19`: https://github.com/collective/collective.syndication/issues/19
