# -*- coding: utf-8 -*-

import re

from django.conf import settings

ire_body = re.compile(re.escape('</body>'), re.IGNORECASE)


class GoogleAnalyticsMiddleware(object):

    def process_response(self, request, response):
        """
        Inject track code just before closing <body>
        """
        content = getattr(response, 'content', None)
        if content is None:
            return response

        # Don't log with debug flag
        if settings.DEBUG:
            return response

        user = getattr(request, 'user', None)

        # Don't log frontend activity of webmaster
        if user and user.is_authenticated() and 'admin' not in request.path:
            return response

        track = "<script> (function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;\
b[l]||(b[l]= function(){(b[l].q=b[l].q||[]).push(arguments)});\
b[l].l=+new Date;\
e=o.createElement(i);\
r=o.getElementsByTagName(i)[0];\
e.src='//www.google-analytics.com/analytics.js';\
r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));\
ga('create','%s');ga('send','pageview');\
</script>" % settings.GOOGLE_ANALYTICS_TOKEN

        content_with_trackcode = ire_body.sub(
            '%s</body>' % track, content)
        response.content = content_with_trackcode
        return response