def pub_start(event):
    path_info = event.request.get('PATH_INFO', "")
    if path_info.endswith('/RSS'):
        event.request.set('PATH_INFO', path_info.replace('/RSS', '/rss.xml'))
