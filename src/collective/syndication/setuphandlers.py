# -*- coding:utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName

PROJECTNAME = 'collective.syndication'
PROFILE_ID = 'profile-collective.syndication:default'


def upgrade_to_1001(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
