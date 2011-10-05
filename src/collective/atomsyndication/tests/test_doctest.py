# -*- coding: utf-8 -*-
import unittest2 as unittest
import doctest

from plone.testing import layered

from collective.atomsyndication.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('controlpanel.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            layer=FUNCTIONAL_TESTING),
        layered(doctest.DocFileSuite('atom.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            layer=FUNCTIONAL_TESTING),
    ])
    return suite
