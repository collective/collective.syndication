import unittest2 as unittest
import doctest

from plone.testing import layered

from collective.atomsyndication.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('README.txt'), layer=FUNCTIONAL_TESTING),
    ])
    return suite
        

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
