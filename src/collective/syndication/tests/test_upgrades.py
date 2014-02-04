# -*- coding: utf-8 -*-

from collective.syndication.setuphandlers import upgrade_to_1001
from collective.syndication.testing import INTEGRATION_TESTING
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest


class Upgradeto1001TestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_update_registry(self):
        registry = getUtility(IRegistry)
        render_body_record = 'collective.syndication.interfaces.ISiteSyndicationSettings.render_body'

        del registry.records[render_body_record]
        self.assertNotIn(render_body_record, registry)

        # run the upgrade step and test registry record is installed
        upgrade_to_1001(self.portal)
        self.assertIn(render_body_record, registry)
