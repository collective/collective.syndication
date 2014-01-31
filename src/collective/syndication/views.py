from DateTime import DateTime
from uuid import uuid3
from uuid import NAMESPACE_OID
from zope.component import getAdapter
from zope.component import getMultiAdapter
from zope.cachedescriptors.property import Lazy as lazy_property
from Products.Five import BrowserView
from zExceptions import NotFound

from collective.syndication.interfaces import ISearchFeed
from collective.syndication.interfaces import IFeed
from collective.syndication.interfaces import IFeedSettings
from collective.syndication.interfaces import ISyndicatable

from collective.syndication import _

from z3c.form import form, button, field
from plone.app.z3cform.layout import wrap_form


class FeedView(BrowserView):

    def feed(self):
        return getAdapter(self.context, IFeed)

    def set_response_header(self):
        # implement in a sub class
        raise NotImplementedError

    def __call__(self):
        util = getMultiAdapter((self.context, self.request),
                               name='syndication-util')
        if util.context_enabled(raise404=True):
            settings = IFeedSettings(self.context)
            if self.__name__ not in settings.feed_types:
                raise NotFound
            index = self.index()
            self.set_response_header()
            return index


class AtomFeedView(FeedView):

    def set_response_header(self):
        self.request.response.setHeader('Content-Type',
                                        'application/atom+xml')


class Rss2FeedView(FeedView):

    def set_response_header(self):
        self.request.response.setHeader('Content-Type',
                                        'text/xml')


class Rss1FeedView(FeedView):

    def set_response_header(self):
        self.request.response.setHeader('Content-Type',
                                        'application/rdf+xml')


class ItunesFeedView(FeedView):

    def set_response_header(self):
        self.request.response.setHeader('Content-Type',
                                        'text/xml')


class SearchFeedView(FeedView):
    def feed(self):
        return getAdapter(self.context, ISearchFeed)

    def __call__(self):
        util = getMultiAdapter((self.context, self.request),
                               name='syndication-util')
        if util.search_rss_enabled(raise404=True):
            self.request.response.setHeader('Content-Type',
                                            'application/rdf+xml')
            return self.index()


class NewsMLFeedView(FeedView):

    def context_enabled(self):
        settings = IFeedSettings(self.context, None)
        if settings and not settings.enabled:
            raise NotFound
        else:
            return True

    @lazy_property
    def current_date(self):
        return DateTime()

    def duid(self, item, value):
        uid = uuid3(NAMESPACE_OID, item.uid + str(value))
        return uid.hex

    def get_image(self, item):
        scales = item.context.restrictedTraverse('@@images')
        if scales:
            try:
                return scales.scale('image')
            except AttributeError:
                pass
        return None

    def newsml_allowed(self):
        util = getMultiAdapter((self.context, self.request),
                               name='syndication-util')
        if not util.site_enabled():
            return False
        elif ISyndicatable.providedBy(self.context):
            settings = IFeedSettings(self.context, None)
            if settings.enabled:
                return True
        return False

    def newsml_enabled(self, raise404=False):
        if not self.newsml_allowed():
            if raise404:
                raise NotFound
            else:
                return False
        else:
            return True

    def __call__(self):
        if self.newsml_enabled(raise404=True):
            settings = IFeedSettings(self.context, None)
            if settings and self.__name__ not in settings.feed_types:
                raise NotFound
            self.request.response.setHeader('Content-Type',
                                            'application/vnd.iptc.g2.newsitem+xml')
            return self.index()


class SettingsForm(form.EditForm):
    label = _(u'heading_syndication_properties',
              default=u'Syndication Properties')
    description = _(
        u'description_syndication_properties',
        default=u'Syndication enables you to syndicate this folder so it can'
        u'be synchronized from other web sites.')
    fields = field.Fields(IFeedSettings)

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
SettingsFormView = wrap_form(SettingsForm)
