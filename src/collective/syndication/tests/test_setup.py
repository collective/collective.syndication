# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.syndication.config import PROJECTNAME
from collective.syndication.testing import INTEGRATION_TESTING
from collective.syndication.setuphandlers import upgrade_to_1001
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('ISyndicationLayer' in layers,
                        'browser layer was not installed')


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('ISyndicationLayer' in layers,
                         'browser layer was not removed')


class Upgradeto1001TestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_update_registry(self):
        """
        """
        registry = getUtility(IRegistry)
        render_body_record = 'collective.syndication.interfaces.ISiteSyndicationSettings.render_body'

        del registry.records[render_body_record]
        self.assertFalse(render_body_record in registry)

        # run the upgrade step and test registry record is installed
        upgrade_to_1001(self.portal)
        self.assertTrue(render_body_record in registry)
