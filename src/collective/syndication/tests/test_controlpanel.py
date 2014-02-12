# -*- coding: utf-8 -*-

from collective.syndication.config import PROJECTNAME
from collective.syndication.controlpanel import ISiteSyndicationSettings
from collective.syndication.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view(u'syndication-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@syndication-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('syndication', actions, 'control panel not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()
                   if a.visible]
        self.assertNotIn('syndication', actions, 'control panel not removed')


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISiteSyndicationSettings)

    def test_allowed_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'allowed'))
        self.assertTrue(self.settings.allowed)

    def test_default_enabled_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'default_enabled'))
        self.assertFalse(self.settings.default_enabled)

    def test_search_rss_enabled_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'search_rss_enabled'))
        self.assertTrue(self.settings.search_rss_enabled)

    def test_show_author_info_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'show_author_info'))
        self.assertTrue(self.settings.show_author_info)

    def test_render_body_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'render_body'))
        self.assertFalse(self.settings.render_body)

    def test_max_items_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'max_items'))
        self.assertEqual(self.settings.max_items, 15)

    def test_allowed_feed_types_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'allowed_feed_types'))
        expected_feed_types = (
            'RSS|RSS 1.0',
            'rss|RSS 2.0',
            'rss.xml|RSS 2.0',
            'atom.xml|Atom',
            'itunes.xml|iTunes',
            'newsml.xml|NewsML 1.2',
        )
        self.assertEqual(self.settings.allowed_feed_types, expected_feed_types)

    def test_site_rss_items_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'site_rss_items'))
        self.assertEqual(self.settings.site_rss_items, ('/news/aggregator',))

    def test_show_syndication_button_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'show_syndication_button'))
        self.assertFalse(self.settings.show_syndication_button)

    def test_show_syndication_link_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'show_syndication_link'))
        self.assertFalse(self.settings.show_syndication_link)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        BASE_REGISTRY = 'collective.syndication.controlpanel.ISiteSyndicationSettings.'
        records = [
            BASE_REGISTRY + 'allowed',
            BASE_REGISTRY + 'default_enabled',
            BASE_REGISTRY + 'search_rss_enabled',
            BASE_REGISTRY + 'show_author_info',
            BASE_REGISTRY + 'render_body',
            BASE_REGISTRY + 'max_items',
            BASE_REGISTRY + 'allowed_feed_types',
            BASE_REGISTRY + 'site_rss_items',
            BASE_REGISTRY + 'show_syndication_button',
            BASE_REGISTRY + 'show_syndication_link',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
