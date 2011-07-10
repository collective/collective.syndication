import unittest
import doctest

from zope.testing import doctestunit
from Testing import ZopeTestCase as ztc

from collective.atomsyndication.tests import base


class FunctionalTestCase(base.FunctionalTestCase):

    def loginAsAdmin(self):
        from Products.PloneTestCase.setup import portal_owner, default_password

        browser = self.browser
        browser.open(self.portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = portal_owner
        browser.getControl(name='__ac_password').value = default_password
        browser.getControl(name='submit').click()

    def installPackage(self):
        from Products.CMFCore.utils import getToolByName
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        qi.installProduct('collective.atomsyndication')
        return qi.isProductInstalled('collective.atomsyndication')

def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='collective.atomsyndication',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='collective.atomsyndication.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='collective.atomsyndication',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'README.txt', package='collective.atomsyndication',
            test_class=FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
