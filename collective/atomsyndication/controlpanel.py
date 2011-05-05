from five import grok

from zope.interface import Interface
from zope import schema
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.registry.browser import controlpanel

from collective.atomsyndication import _

try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget

from z3c.form.browser.checkbox import CheckBoxFieldWidget

class IAtomSettings(Interface):
    """ Interface for the form on the control panel. """
    atom_enabled = schema.Bool(title=_(u"Enable Atom 1.0 feeds"), description=_(u"Checking this box will create an atom feed at the root of the portal that will include all of the published content within this portal."), required=True, default=True)
#    max_entries = schema.Int(title=_(u"Maximum number of entries on feed"), description=_(u"The maximum number of entries that will be seen on the atom feed."), min=0, required=False, default=None)
    feed_depth = schema.Int(title=_(u"Depth of the site-wide feed"), description=_(u"The number of levels of folders below the portal root to be included in the site-wide atom feed. 0 indicates no limits on depth. 1 indicates that only the root folder will be included."), min=0, required=True, default=0)

class AtomSettingsEditForm(controlpanel.RegistryEditForm):
    grok.context(IPloneSiteRoot)
    grok.name("atom_settings")
    grok.require("cmf.ManagePortal")

    schema = IAtomSettings
    label = _(u"Atom Syndication Settings") 
    description = _(u"Here you can modify the settings for Atom syndication.")

    def updateFields(self):
        super(AtomSettingsEditForm, self).updateFields()
#        self.fields['required_categories'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super(AtomSettingsEditForm, self).updateWidgets()
#        self.widgets['tags'].rows = 8
#        self.widgets['tags'].style = u'width: 30%;'
#        self.widgets['unique_categories'].rows = 8
#        self.widgets['unique_categories'].style = u'width: 30%;'
#        self.widgets['required_categories'].rows = 8
#        self.widgets['required_categories'].style = u'width: 30%;'

class AtomSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = AtomSettingsEditForm
