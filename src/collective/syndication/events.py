def pub_start(event):
    #XXX: When at site root level, if we call 'rss' or 'RSS', we get the
    #     template from portal_skins, so we add @@ here to workaround it.
    path_info = event.request.get('PATH_INFO', "")
    if path_info.endswith('/rss'):
        event.request.set('PATH_INFO', path_info.replace('/rss', '/@@rss'))
    if path_info.endswith('/RSS'):
        event.request.set('PATH_INFO', path_info.replace('/RSS', '/@@RSS'))
