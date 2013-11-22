import re
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests import PloneTestCase
from collective.syndication.interfaces import IFeedSettings
from collective.syndication.interfaces import ISiteSyndicationSettings
from plone.registry.interfaces import IRegistry
from zope.component import getAdapter
from zope.component import getUtility
from zExceptions import NotFound
from collective.syndication.interfaces import IFeed
from collective.syndication.interfaces import INewsMLFeed
from collective.syndication.adapters import BaseItem
from collective.syndication.adapters import BaseNewsMLItem
from collective.syndication.testing import INTEGRATION_TESTING
from plone.dexterity.fti import DexterityFTI
from zope.interface import Interface
from plone.app.textfield import RichText


class BaseSyndicationTest(PloneTestCase.PloneTestCase):

    layer = INTEGRATION_TESTING

    def afterSetUp(self):
        self.syndication = getToolByName(self.portal, 'portal_syndication')
        self.folder.invokeFactory('Document', 'doc1')
        self.folder.invokeFactory('Document', 'doc2')
        self.folder.invokeFactory('File', 'file')
        self.doc1 = self.folder.doc1
        self.doc2 = self.folder.doc2
        self.file = self.folder.file
        #Enable syndication on folder
        registry = getUtility(IRegistry)
        self.site_settings = registry.forInterface(ISiteSyndicationSettings)
        settings = IFeedSettings(self.folder)
        settings.enabled = True
        self.folder_settings = settings


class TestSyndicationUtility(BaseSyndicationTest):

    layer = INTEGRATION_TESTING

    def test_context_allowed_not_syndicatable(self):
        util = self.folder.file.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.context_allowed(), False)

    def test_context_allowed(self):
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.context_allowed(), True)

    def test_context_allowed_site_disabled(self):
        self.site_settings.allowed = False
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.context_allowed(), False)

    def test_context_enabled(self):
        self.folder_settings.enabled = True
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.context_enabled(), True)

    def test_not_context_enabled(self):
        self.folder_settings.enabled = False
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.context_enabled(), False)

    def test_context_enabled_site_disabled(self):
        self.site_settings.allowed = False
        self.folder_settings.enabled = True
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.context_enabled(), False)

    def test_context_enabled_raises_404(self):
        self.site_settings.allowed = False
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertRaises(NotFound, util.context_enabled, True)

    def test_allowed_feed_types(self):
        util = self.folder.restrictedTraverse('@@syndication-util')
        types = util.allowed_feed_types()
        self.assertEqual(len(types), len(self.folder_settings.feed_types))

    def test_site_settings(self):
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertTrue(util.site_settings is not None)

    def test_search_rss_enabled(self):
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.site_settings.search_rss_enabled = True
        self.assertEqual(util.search_rss_enabled(), True)

    def test_not_search_rss_enabled_raise_404(self):
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.site_settings.search_rss_enabled = False
        self.assertRaises(NotFound, util.search_rss_enabled, True)

    def test_show_author_info(self):
        self.site_settings.show_author_info = True
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.show_author_info(), True)
        self.site_settings.show_author_info = False
        self.assertEqual(util.show_author_info(), False)


class TestSyndicationViews(BaseSyndicationTest):

    layer = INTEGRATION_TESTING

    def test_valid_feeds(self):
        for _type in self.folder_settings.feed_types:
            if str(_type) not in ["RSS", "rss"]:
                # RSS and rss are special cases that redirect to @@RSS and
                # @@rss respectively. see events.py for more details
                self.folder.restrictedTraverse(str(_type))()

    def test_invalid_feed_raises_404(self):
        self.folder_settings.feed_types = ('RSS',)
        self.assertRaises(NotFound, self.folder.restrictedTraverse('rss.xml'))

    def test_search_feed_view(self):
        self.site_settings.search_rss_enabled = True
        self.portal.restrictedTraverse('@@search_rss')()

    def test_search_feed_view_raises_404(self):
        self.site_settings.search_rss_enabled = False
        self.assertRaises(NotFound,
                          self.portal.restrictedTraverse('@@search_rss'))

    def test_proper_response_headers(self):
        self.folder_settings.feed_types = ('RSS',
                                           'rss',
                                           'rss.xml',
                                           'atom.xml',
                                           'newsml.xml',
                                           'itunes.xml')
        self.folder.restrictedTraverse("@@RSS")()
        header = self.folder.REQUEST.response.getHeader("Content-Type")
        self.assertEqual(header, "application/rdf+xml")
        self.folder.restrictedTraverse("@@rss")()
        header = self.folder.REQUEST.response.getHeader("Content-Type")
        self.assertEqual(header, "application/rdf+xml")
        self.folder.restrictedTraverse("@@rss.xml")()
        header = self.folder.REQUEST.response.getHeader("Content-Type")
        self.assertEqual(header, "text/xml")
        self.folder.restrictedTraverse("@@atom.xml")()
        header = self.folder.REQUEST.response.getHeader("Content-Type")
        self.assertEqual(header, "application/atom+xml")
        self.folder.restrictedTraverse("@@newsml.xml")()
        header = self.folder.REQUEST.response.getHeader("Content-Type")
        self.assertEqual(header, "application/vnd.iptc.g2.newsitem+xml")
        self.folder.restrictedTraverse("@@itunes.xml")()
        header = self.folder.REQUEST.response.getHeader("Content-Type")
        self.assertEqual(header, "text/xml")


class TestSyndicationFeedAdapter(BaseSyndicationTest):

    layer = INTEGRATION_TESTING

    def afterSetUp(self):
        super(TestSyndicationFeedAdapter, self).afterSetUp()
        self.feed = IFeed(self.folder)
        self.feeddatadoc = BaseItem(self.doc1, self.feed)
        self.feeddatafile = BaseItem(self.file, self.feed)

    def test_link_on_folder(self):
        self.assertEqual(self.feed.link, self.folder.absolute_url())

    def test_link_on_file(self):
        self.assertEqual(self.feeddatafile.link,
                         self.file.absolute_url() + '/view')

    def test_items(self):
        self.assertEqual(len(self.feed._brains()), 3)
        self.assertEqual(len([i for i in self.feed.items]), 3)

    def test_has_enclosure(self):
        self.assertEqual(self.feeddatadoc.has_enclosure, False)
        self.assertEqual(self.feeddatafile.has_enclosure, True)


BODY_TEXT = """<p>Test text</p>
<h2>Header</h2>
<p class="one" id="test">New <span>Line</span></p>
<a href="http://www.google.com" class="new">Google</a>
<ol><li>one</li><li>two</li></ol>
<ul><li>one</li><li>two</li></ul>
"""
ROOTED_BODY_TEXT = """<body>
<p>Test text</p>
<h2>Header rooted</h2>
<p class="one" id="test">New <span>Line</span></p>
<a href="http://www.google.com" class="new">Google</a>
<ol><li>one</li><li>two</li></ol>
<ul><li>one</li><li>two</li></ul>
</body>
"""


class NewsMLBaseSyndicationTest(PloneTestCase.PloneTestCase):

    layer = INTEGRATION_TESTING

    def afterSetUp(self):
        self.syndication = getToolByName(self.portal, 'portal_syndication')
        self.folder.invokeFactory('Document', 'doc')
        self.folder.invokeFactory('Document', 'doc1')
        self.folder.invokeFactory('News Item', 'news1')
        self.folder.invokeFactory('News Item', 'news2')
        self.folder.invokeFactory('File', 'file')
        self.doc1 = self.folder.doc1
        self.news1 = self.folder.news1
        self.news1.setText(BODY_TEXT)
        self.news2 = self.folder.news2
        self.news2.setText(ROOTED_BODY_TEXT)
        self.file = self.folder.file
        #Enable syndication on folder
        registry = getUtility(IRegistry)
        self.site_settings = registry.forInterface(ISiteSyndicationSettings)
        settings = IFeedSettings(self.folder)
        settings.enabled = True
        self.folder_settings = settings


class TestNewsMLSyndicationUtility(NewsMLBaseSyndicationTest):

    layer = INTEGRATION_TESTING

    def test_newsml_allowed_not_syndicatable(self):
        util = self.folder.file.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_allowed(), False)

    def test_newsml_allowed(self):
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_allowed(), True)
        util = self.news1.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_allowed(), True)

    def test_newsml_allowed_site_disabled(self):
        self.site_settings.allowed = False
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_allowed(), False)
        util = self.news1.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_allowed(), False)

    def test_newsml_enabled(self):
        self.folder_settings.enabled = True
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_enabled(), True)
        util = self.news1.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_enabled(), True)

    def test_not_newsml_enabled(self):
        self.folder_settings.enabled = False
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_enabled(), False)

    def test_newsml_enabled_site_disabled(self):
        self.site_settings.allowed = False
        self.folder_settings.enabled = True
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_enabled(), False)
        util = self.news1.restrictedTraverse('@@syndication-util')
        self.assertEqual(util.newsml_enabled(), False)

    def test_newsml_enabled_raises_404(self):
        self.site_settings.allowed = False
        util = self.folder.restrictedTraverse('@@syndication-util')
        self.assertRaises(NotFound, util.newsml_enabled, True)
        util = self.folder.news1.restrictedTraverse('@@syndication-util')
        self.assertRaises(NotFound, util.newsml_enabled, True)


class TestNewsMLSyndicationFeedAdapter(NewsMLBaseSyndicationTest):

    layer = INTEGRATION_TESTING

    def afterSetUp(self):
        super(TestNewsMLSyndicationFeedAdapter, self).afterSetUp()

        self.feed = INewsMLFeed(self.folder)
        self.feeddatnews1 = BaseNewsMLItem(self.news1, self.feed)
        self.feeddatnews2 = BaseNewsMLItem(self.news2, self.feed)

    def test_items(self):
        self.assertEqual(len(self.feed._brains()), 5)
        self.assertEqual(len([i for i in self.feed.items]), 2)

    def test_filter_body(self):
        output = '<p>Test text</p><p>Header</p><p>New Line</p><a href="http://www.google.com">Google</a><ul><li>one</li><li>two</li></ul><ul><li>one</li><li>two</li></ul>'
        self.assertEqual(self.feeddatnews1.body, output)
        output = '<p>Test text</p><p>Header rooted</p><p>New Line</p><a href="http://www.google.com">Google</a><ul><li>one</li><li>two</li></ul><ul><li>one</li><li>two</li></ul>'
        self.assertEqual(self.feeddatnews2.body, output)

    def test_image_caption(self):
        self.news1.image = "Image"

        self.assertEqual(self.feeddatnews1.image_caption, "")

        self.news1.setDescription("News description")
        self.assertEqual(self.feeddatnews1.image_caption, "News description")

        self.news1.imageCaption = "Image caption"
        self.assertEqual(self.feeddatnews1.image_caption, "Image caption")

    def test_created_date(self):
        self.assertEqual(self.feeddatnews1.created, self.news1.created())


class ITestSchema(Interface):
    """Schema used for testing
    """

    text = RichText(
        # nitf/body/body.content
        title=u'Body text',
        required=False,
    )


class TestDexterityItems(BaseSyndicationTest):

    layer = INTEGRATION_TESTING

    def afterSetUp(self):
        super(TestDexterityItems, self).afterSetUp()
        portal = self.portal
        fti = DexterityFTI('dxtest_type')
        fti.schema = u'collective.syndication.tests.test_syndication.ITestSchema'
        portal.portal_types._setObject('dxtest_type', fti)
        self.folder.invokeFactory('dxtest_type', 'dxtest1')
        self.folder.dxtest1.text = u'<p>Lorem ipsum dolor sit amet.</p>'

    def test_body(self):
        feed = getAdapter(self.folder, IFeed)
        self.assertTrue(u'<p>Lorem ipsum dolor sit amet.</p>' == tuple(feed.items)[-1].body)


class TestRenderBody(BaseSyndicationTest):

    layer = INTEGRATION_TESTING

    def afterSetUp(self):
        super(TestRenderBody, self).afterSetUp()
        self.folder.invokeFactory('News Item', 'news1')
        self.folder.invokeFactory('News Item', 'news2')
        self.news1 = self.folder.news1
        self.news1.setTitle('News 1')
        self.news1.setDescription('The news item #1')
        self.news1.setText(BODY_TEXT)
        self.news2 = self.folder.news2
        self.news2.setTitle('News 2')
        self.news2.setText(ROOTED_BODY_TEXT)
        #Enable syndication on folder
        registry = getUtility(IRegistry)
        self.site_settings = registry.forInterface(ISiteSyndicationSettings)
        settings = IFeedSettings(self.folder)
        settings.enabled = True
        settings.render_body = True
        self.folder_settings = settings

    def test_atom(self):
        xml = self.folder.restrictedTraverse("@@atom.xml")()
        self.assertTrue(len(re.findall('<entry>', xml)) == 5)
        news1_feed = '<entry>\s*<title>News 1</title>\s*' \
                     '<link rel="alternate" type="text/html" href="{0}"/>\s*' \
                     '<id>urn:syndication:{1}</id>\s*' \
                     '<summary>The news item #1</summary>\s*' \
                     '<content type="xhtml" xml:base="{2}" xml:lang="en" xml:space="preserve">'.format(self.news1.absolute_url(),
                                                                                                       self.news1.UID(),
                                                                                                       self.folder.absolute_url())
        self.assertTrue(re.search(news1_feed, xml) is not None)
        self.assertTrue(re.search(BODY_TEXT, xml) is not None)
        news2_feed = '<entry>\s*<title>News 2</title>\s*' \
                     '<link rel="alternate" type="text/html" href="{0}"/>\s*' \
                     '<id>urn:syndication:{1}</id>\s*' \
                     '<content type="xhtml" xml:base="{2}" xml:lang="en" xml:space="preserve">'.format(self.news2.absolute_url(),
                                                                                                       self.news2.UID(),
                                                                                                       self.folder.absolute_url())
        self.assertTrue(re.search(news2_feed, xml) is not None)
        self.assertFalse(re.search(ROOTED_BODY_TEXT, xml) is not None)
        self.assertTrue(re.search('<h2>Header rooted</h2>', xml) is not None)

    def test_rss1(self):
        xml = self.folder.restrictedTraverse("@@RSS")()
        self.assertTrue(len(re.findall('<item ', xml)) == 5)
        news_feed = '<item rdf:about="{0}">\s*<title>News 1</title>\s*' \
                    '<link>{0}</link>\s*' \
                    '<description>The news item #1</description>\s*' \
                    '<content:encoded xmlns:content="http://purl.org/rss/1.0/modules/content/"'.format(self.news1.absolute_url())
        self.assertTrue(re.search(news_feed, xml) is not None)
        news_feed = '<item rdf:about="{0}">\s*<title>News 2</title>\s*' \
                    '<link>{0}</link>\s*' \
                    '<description></description>\s*' \
                    '<content:encoded xmlns:content="http://purl.org/rss/1.0/modules/content/"'.format(self.news2.absolute_url())
        self.assertTrue(re.search(news_feed, xml) is not None)

    def test_rss2(self):
        xml = self.folder.restrictedTraverse("@@rss.xml")()
        self.assertTrue(len(re.findall('<item>', xml)) == 5)
        news_feed = '<item>\s*<title>News 1</title>\s*' \
                    '<description>The news item #1</description>\s*' \
                    '<content:encoded xmlns:content="http://purl.org/rss/1.0/modules/content/"'
        self.assertTrue(re.search(news_feed, xml) is not None)
        news_feed = '<item>\s*<title>News 2</title>\s*' \
                    '<description></description>\s*' \
                    '<content:encoded xmlns:content="http://purl.org/rss/1.0/modules/content/"'
        self.assertTrue(re.search(news_feed, xml) is not None)
