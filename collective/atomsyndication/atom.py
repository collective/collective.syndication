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
        if getattr(self.request, 'RESPONSE', None):
            self.request.RESPONSE.setHeader('Content-Type', 'application/atom+xml;;charset=utf-8')
        syn_tool = getToolByName(self.context, 'portal_syndication')
        self.results= syn_tool.getSyndicatableContent(self.context)

    def filter_syndicatable(self, results):
        syn_tool = getToolByName(self.context, 'portal_syndication')
        filtered = {}
        intermed = []
        for res in results:
            obj = res.getObject()
            if syn_tool.isSyndicationAllowed(obj):
                obj_name = res['id']
                obj_label = res['Title']
                limit = syn_tool.getMaxItems(obj)
                objlist = list(syn_tool.getSyndicatableContent(obj))[:limit]
                for sobj in objlist:
                    uid = sobj.UID
                    if filtered.has_key(uid):
                        filtered[uid]['categories'].append((obj_name, obj_label))
                    else:
                        filtered[uid] = {'categories': [(obj_name, obj_label),], 'object': obj}
                    intermed.append(sobj)
        self.filtered = filtered
        return intermed

    def query_catalog(self, query):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(query)

    def atom_id_tag(self, context):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        root_url = portal_state.portal_url()
        mod_date = context.ModificationDate
        url = self.url_parser(root_url)
        tag = u"tag:%s,%s:%s" % (url[0], context.ModificationDate[:10], context.UID)
        return tag

    def url_parser(self, data):
        p = re.compile(r'https?://')
        p1 = p.sub('', data)
        p2 = p1.split('/')
        return p2

class RootAtomFeedView(AtomFeedView):
    grok.context(IPloneSiteRoot)

    def update(self):
        if getattr(self.request, 'RESPONSE', None):
            self.request.RESPONSE.setHeader('Content-Type', 'application/atom+xml;;charset=utf-8')
        q_results = self.query_catalog({'portal_type': ('Topic', 'Folder',)})
        self.results = self.filter_syndicatable(q_results)
