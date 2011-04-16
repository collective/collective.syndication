README.txt
==========

    >>> self.installPackage()
    True
    >>> from Products.CMFPlone.utils import _createObjectByType
    >>> _createObjectByType(type_name="Topic", container=self.portal, id="atomic", title=u"Atomic Content", description=u"A collection of atomic content.")
    <ATTopic at /plone/atomic>
    >>> atomic = self.portal['atomic']
    >>> from Products.Five.testbrowser import Browser
    >>> self.browser = Browser()

    >>> self.loginAsAdmin()
    >>> self.browser.open(atomic.absolute_url()+'/atom.xml')
    >>> self.browser.url
    'http://nohost/plone/atomic/atom.xml'
    >>> self.browser.headers["Content-type"]
    'application/atom+xml;charset=utf-8'
    >>> u'<title>Atomic Content</title>' in self.browser.contents
    True


