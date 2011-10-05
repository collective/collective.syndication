# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.atomsyndication.config import PROJECTNAME
from collective.atomsyndication.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.failUnless('IAtomSyndicationLayer' in layers)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_uninstalled(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        qi.uninstallProducts(products=[PROJECTNAME])
        self.failIf(qi.isProductInstalled(PROJECTNAME))

    # FIXME: need to apply uninstall profile
    def test_browserlayer_uninstalled(self):
        layers = [l.getName() for l in registered_layers()]
        self.failIf('IAtomSyndicationLayer' in layers)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
