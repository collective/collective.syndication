from five import grok
from zope.interface import Interface
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from Products.ATContentTypes.interfaces.interfaces import IATContentType
grok.templatedir('templates')

class IAtomSyndicationLayer(IDefaultBrowserLayer):
    """ Default browser layer for the package. """

class AtomFeedView(grok.View):
    grok.context(Interface)
    grok.name('atom.xml')
    grok.template('atom')
    grok.layer(IAtomSyndicationLayer)

    def update(self):
        self.request.RESPONSE.setHeader('Content-Type', 'application/atom+xml;;charset=utf-8')

class AtomLinkViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IHtmlHeadLinks)
    grok.name('plone.links.atom')
    grok.template('atom_link')
    grok.layer(IAtomSyndicationLayer)

    def update(self):
        syntool = getToolByName(self.context, 'portal_syndication')
        if syntool.isSyndicationAllowed(self.context):
            self.allowed = True
            context_state = getMultiAdapter((self.context, self.request),
            name=u'plone_context_state')
            self.url = '%s/atom.xml' % context_state.object_url()
        else:
            self.allowed = False
