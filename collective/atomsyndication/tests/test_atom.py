
import sys
import unittest
import logging

from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest
from Products.CMFCore.utils import getToolByName

from collective.atomsyndication import atom
from collective.atomsyndication.tests import base

logging.basicConfig()
logger = logging.getLogger('collective.atomsyndication')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug(u'\nBegin collective.syndication LOG')

PROJECTNAME = 'collective.atomsyndication'
CONTENT_STRUCTURE = (dict(type='Topic',
                          id='news-1',
                          title=u"News Article Number One",
                          description=u"A brief description about the\
                                  artcile, explaining things\
                                  about stuff."
                                  ),
                                  
                     dict(type='Topic',
                          id='news-2',
                          title=u"News Article Number Two",
                          description=u"A brief description about the\
                                  artcile, explaining things\
                                  about stuff."),
                    )
class TestSetup(base.IntegrationTestCase):
    """ Checks instalation of this product """

    def afterSetup(self):
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def populateSite(self):
        for item in CONTENT_STRUCTURE:
            self.folder.invokeFactory(item["type"],
                                    id=item["id"],
                                    title=item["title"],
                                    description=item["description"],
                                    )
            self.folder[item["id"]].reindexObject()

    def test_atom_installed(self):
        self.addProfile('collective.atomsyndication:default')
        portal_quickinstaller = self.portal.portal_quickinstaller
        self.failUnless(portal_quickinstaller.isProductInstalled(PROJECTNAME),
                                            '%s not installed' % PROJECTNAME)


    def test_root_atom_enabled(self):
        self.loginAsPortalOwner()
        self.addProfile('collective.atomsyndication:default')
        self.populateSite()
        req = TestRequest()
        #view = getMultiAdapter((self.portal, TestRequest()), name=u"atom.xml")
        view = atom.RootAtomFeedView(self.portal, None)
        #view = self.portal.restrictedTraverse("atom.xml")
        view.update()
        logger.debug(u"\nResults: %s" % view.results)
        rendered = view.render()
        logger.debug(u"\nView: %s" % view.render())



def test_suite():
    suite= unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
