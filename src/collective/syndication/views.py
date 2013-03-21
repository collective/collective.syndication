from zope.component import getAdapter
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from zExceptions import NotFound

from collective.syndication.interfaces import ISearchFeed
from collective.syndication.interfaces import IFeed
from collective.syndication.interfaces import IFeedSettings
from collective.syndication.interfaces import INewsMLFeed

from collective.syndication import _

from z3c.form import form, button, field
from plone.app.z3cform.layout import wrap_form


class FeedView(BrowserView):

    def feed(self):
        return getAdapter(self.context, IFeed)

    def __call__(self):
        util = getMultiAdapter((self.context, self.request),
                               name='syndication-util')
        if util.context_enabled(raise404=True):
            settings = IFeedSettings(self.context)
            if self.__name__ not in settings.feed_types:
                raise NotFound
            self.request.response.setHeader('Content-Type',
                                            'application/atom+xml')
            return self.index()


class SearchFeedView(FeedView):
    def feed(self):
        return getAdapter(self.context, ISearchFeed)

    def __call__(self):
        util = getMultiAdapter((self.context, self.request),
                               name='syndication-util')
        if util.search_rss_enabled(raise404=True):
            self.request.response.setHeader('Content-Type',
                                            'application/atom+xml')
            return self.index()


class NewsMLFeedView(BrowserView):

    def feed(self):
        return getAdapter(self.context, INewsMLFeed)

    def context_enabled(self):
        settings = IFeedSettings(self.context, None)
        if settings and not settings.enabled:
            raise NotFound
        else:
            return True

    def __call__(self):
        util = getMultiAdapter((self.context, self.request),
                               name='syndication-util')
        if util.newsml_enabled(raise404=True):
            settings = IFeedSettings(self.context, None)
            if settings and self.__name__ not in settings.feed_types:
                raise NotFound
            self.request.response.setHeader('Content-Type',
                                            'application/atom+xml')
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
