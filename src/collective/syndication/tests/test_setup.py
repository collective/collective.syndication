# -*- coding: utf-8 -*-

from collective.syndication.config import PROJECTNAME
from collective.syndication.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest2 as unittest


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_is_registered(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('ISyndicationLayer', layers)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_is_unregistered(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('ISyndicationLayer', layers)
