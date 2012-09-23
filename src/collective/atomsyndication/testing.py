# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

try:
    # Try to get the new collection type
    import plone.app.collection
    HAS_COLLECTION = True
except:
    HAS_COLLECTION = False


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.atomsyndication
        self.loadZCML(package=collective.atomsyndication)
        if HAS_COLLECTION:
            self['has_collection'] = True
        else:
            self['has_collection'] = False

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.atomsyndication:default')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.atomsyndication:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.atomsyndication:Functional',
    )
