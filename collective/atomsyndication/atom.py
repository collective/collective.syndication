import re
from five import grok

from zope.interface import Interface
from zope.component import getMultiAdapter, getUtility
from Products.CMFCore.utils import getToolByName

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks

from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.registry.interfaces import IRegistry
from collective.atomsyndication.controlpanel import IAtomSettings

grok.templatedir('templates')

class IAtomSyndicationLayer(IDefaultBrowserLayer):
    """ Default browser layer for the package. """

class AtomLinkViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IHtmlHeadLinks)
    grok.name('plone.links.atom')
    grok.template('atom_link')
    grok.layer(IAtomSyndicationLayer)

    def update(self):
        syntool = getToolByName(self.context, 'portal_syndication')
        registry = getUtility(IRegistry)
        self.atom_settings = registry.forInterface(IAtomSettings)
        self.allowed = False
        if self.atom_settings.atom_enabled:
            context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
            if syntool.isSyndicationAllowed(self.context):
                self.allowed = True
                self.url = '%s/atom.xml' % context_state.object_url()
            if context_state.is_portal_root():
                self.allowed = True
                self.url = '%s/atom.xml' % context_state.canonical_object_url()

class AtomFeedView(grok.View):
    grok.context(Interface)
    grok.name('atom.xml')
    grok.template('atom')
    grok.layer(IAtomSyndicationLayer)

    def update(self):
        self.request.RESPONSE.setHeader('Content-Type', 'application/atom+xml;;charset=utf-8')
        registry = getUtility(IRegistry)
        self.atom_settings = registry.forInterface(IAtomSettings)
        if IPloneSiteRoot.providedBy(self.context):
            self.results = self.query_catalog({'review_state': 'published', 'portal_type': ('Collection', 'Folder')})
        else:
            syn_tool = getToolByName(self.context, 'portal_syndication')
            self.results = syn_tool.getSyndicatableContent(self.context)
            #            self.results = self.query_catalog({'path': {'query': '/'.join(this_path), 'depth': 1},})

    def query_catalog(self, query):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(query)

    def atom_id_tag(self, context):
        url_tool = getToolByName(self.context, 'portal_url')
        portal = url_tool.getPortalObject()
        root_url = portal.absolute_url()
        cre_date = context.CreationDate()
        mod_date = context.ModificationDate()
        tag = u"tag:%s," % self.remove_proto(root_url)
        return tag

    def remove_proto(self, data):
        p = re.compile(r'https?://')
        p1 = p.sub('', data)
        p2 = p1.split('/')

    def getNavTree(self, _marker=[]):
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)
