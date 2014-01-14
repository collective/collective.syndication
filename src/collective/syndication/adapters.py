from uuid import uuid3
from uuid import NAMESPACE_URL

from zope.component.hooks import getSite
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements, Interface
from zope.component import queryMultiAdapter

from DateTime import DateTime
from OFS.interfaces import IItem

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.syndication.interfaces import IFeed
from collective.syndication.interfaces import IFeedItem
from collective.syndication.interfaces import ISearchFeed
from collective.syndication.interfaces import IFeedSettings

from Products.ATContentTypes.interfaces.file import IFileContent
from plone.uuid.interfaces import IUUID
from zope.cachedescriptors.property import Lazy as lazy_property

# this might be a little silly but it's possible to not use
# Products.CMFPlone with dexterity content types
try:
    from plone.dexterity.interfaces import IDexterityContent
except ImportError:
    class IDexterityContent(Interface):  # NOQA
        pass
try:
    from plone.rfc822.interfaces import IPrimaryFieldInfo
except ImportError:
    class IPrimaryFieldInfo(Interface):  # NOQA
        pass
try:
    from plone.namedfile.interfaces import INamedField
except ImportError:
    class INamedField(Interface):  # NOQA
        pass


class BaseFeedData(object):

    def __init__(self, context):
        self.context = context
        self.settings = IFeedSettings(context)
        self.site = getSite()
        self.pm = getToolByName(self.context, 'portal_membership')
        pprops = getToolByName(self.context, 'portal_properties')
        self.site_props = pprops.site_properties
        self.view_action_types = self.site_props.getProperty(
            'typesUseViewActionInListings', ('File', 'Image'))

    @lazy_property
    def show_about(self):
        return self.settings.show_author_info

    @property
    def link(self):
        return self.base_url

    @lazy_property
    def base_url(self):
        return self.context.absolute_url()

    @property
    def title(self):
        return self.context.Title()

    @property
    def description(self):
        return self.context.Description()

    @property
    def categories(self):
        return self.context.Subject()

    @property
    def published(self):
        date = self.context.EffectiveDate()
        if date and date != 'None':
            return DateTime(date)

    @property
    def modified(self):
        date = self.context.ModificationDate()
        if date:
            return DateTime(date)

    @property
    def uid(self):
        uuid = IUUID(self.context, None)
        if uuid is None and hasattr(self.context, 'UID'):
            return self.context.UID()
        return uuid

    @property
    def rights(self):
        return self.context.Rights()

    @property
    def publisher(self):
        if hasattr(self.context, 'Publisher'):
            return self.context.Publisher()
        return 'No Publisher'


class FolderFeed(BaseFeedData):
    implements(IFeed)

    @lazy_property
    def author(self):
        if self.show_about:
            creator = self.context.Creator()
            member = self.pm.getMemberById(creator)
            return member

    @property
    def author_name(self):
        if self.author:
            return self.author.getProperty('fullname')

    @property
    def author_email(self):
        if self.author:
            return self.author.getProperty('email')

    @property
    def logo(self):
        return '%s/logo.png' % self.site.absolute_url()

    @property
    def icon(self):
        return '%s/favicon.ico' % self.site.absolute_url()

    def _brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(path={
            'query': '/'.join(self.context.getPhysicalPath()),
            'depth': 1
        })[:self.limit]

    def _items(self):
        """
        do catalog query
        """
        return [b.getObject() for b in self._brains()]

    @property
    def items(self):
        for item in self._items():
            # look for custom adapter
            # otherwise, just use default
            adapter = queryMultiAdapter((item, self), IFeedItem)
            if adapter is None:
                adapter = BaseItem(item, self)
            yield adapter

    @property
    def limit(self):
        return self.settings.max_items

    @property
    def language(self):
        langtool = getToolByName(self.context, 'portal_languages')
        return langtool.getDefaultLanguage()


class CollectionFeed(FolderFeed):
    def _brains(self):
        return self.context.queryCatalog(batch=False)[:self.limit]


class SearchFeed(FolderFeed):
    implements(ISearchFeed)

    def _brains(self):
        max_items = self.limit
        request = self.context.REQUEST
        start = int(request.get('b_start', 0))
        end = int(request.get('b_end', start + max_items))
        request.set('sort_order', 'reverse')
        request.set('sort_on', request.get('sort_on', 'effective'))
        return self.context.queryCatalog(show_all=1, use_types_blacklist=True,
                                         use_navigation_root=True)[start:end]


class RootFeed(SearchFeed):

    @property
    def uid(self):
        uuid = super(RootFeed, self).uid
        if not uuid:
            # Portal Root doesn't have an UUID, so we forge one up from the url
            uuid = uuid3(NAMESPACE_URL, self.link).hex
        return uuid

    def _brains(self):
        request = self.context.REQUEST
        util = getMultiAdapter((self.context, request), name="syndication-util")
        site_rss_items = util.site_settings.site_rss_items

        ucatalog = getToolByName(self.context, 'uid_catalog')

        uids = ucatalog(UID=site_rss_items)
        paths = ['/'.join(i.getObject().getPhysicalPath()) for i in uids]

        if paths != []:
            request.set('path', paths)
        return super(RootFeed, self)._brains()


class BaseItem(BaseFeedData):
    implements(IFeedItem)
    adapts(IItem, IFeed)

    def __init__(self, context, feed):
        self.context = context
        self.feed = feed
        self.pm = self.feed.pm

    @lazy_property
    def creator(self):
        if hasattr(self.context, 'Creator'):
            return self.context.Creator()

    @lazy_property
    def author(self):
        member = self.pm.getMemberById(self.creator)
        return member

    @property
    def author_name(self):
        author = self.author
        if author and hasattr(author, 'getProperty'):
            return author.getProperty('fullname')

    @property
    def author_email(self):
        author = self.author
        if author and hasattr(author, 'getProperty'):
            return author.getProperty('email')

    @property
    def body(self):
        if hasattr(self.context, 'getText'):
            return self.context.getText()
        elif hasattr(self.context, 'text'):
            if isinstance(self.context.text, (str, unicode)):
                return self.context.text
            elif hasattr(self.context.text, 'output'):
                return self.context.text.output
        return self.description

    content_core_template = ViewPageTemplateFile("templates/content_core.pt")

    def render_content_core(self):
        self.request = self.context.REQUEST
        return self.content_core_template()

    @property
    def link(self):
        url = self.base_url
        if self.context.portal_type in self.feed.view_action_types:
            url = url + '/view'
        return url

    guid = link

    @property
    def has_enclosure(self):
        return IFileContent.providedBy(self.context)

    @lazy_property
    def file(self):
        if self.has_enclosure:
            return self.context.getFile()

    @property
    def file_url(self):
        url = self.base_url
        fi = self.file
        if fi is not None:
            filename = fi.getFilename()
            if filename:
                url += '/@@download/file/' + filename
        return url

    @property
    def file_length(self):
        return self.file.get_size()

    @property
    def file_type(self):
        return self.file.getContentType()


class DexterityItem(BaseItem):
    adapts(IDexterityContent, IFeed)

    def __init__(self, context, feed):
        super(DexterityItem, self).__init__(context, feed)
        self.dexterity = IDexterityContent.providedBy(context)
        try:
            self.primary = IPrimaryFieldInfo(self.context)
        except TypeError:
            self.primary = None

    @property
    def file_url(self):
        url = self.base_url
        fi = self.file
        if fi is not None:
            filename = fi.filename
            if filename:
                url += '/@@download/%s/%s' % (
                    self.primary.field.__name__, filename)
        return url

    @property
    def has_enclosure(self):
        if self.primary:
            return INamedField.providedBy(self.primary.field)
        else:
            return False

    @lazy_property
    def file(self):
        if self.has_enclosure:
            return self.primary.field.get(self.context)

    @property
    def file_length(self):
        return self.file.getSize()

    @property
    def file_type(self):
        return self.file.contentType
