# -*- coding: utf-8 -*-
import unittest
import doctest

from Testing import ZopeTestCase as ztc
from collective.atomsyndication.tests.test_browser import FunctionalTestCase


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite('tests/atom.txt',
            package='collective.atomsyndication',
            test_class=FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        #ztc.ZopeDocFileSuite('tests/controlpanel.txt',
        #    package='collective.atomsyndication',
        #    test_class=base.FunctionalTestCase,
        #    optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])
