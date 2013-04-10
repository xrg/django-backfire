from django.conf import settings
from django.middleware.csrf import get_token
from django.core.urlresolvers import reverse

EXCLUDE_DIRS = (reverse('admin:index'), settings.MEDIA_URL, settings.STATIC_URL)

class BackfireMiddleware(object):
    def process_response(self, request, response):
        if request.path.startswith( EXCLUDE_DIRS ):
            return response

        try:
            if request.user.is_staff and response['Content-Type'].split(';', 1)[0] == 'text/html':
                html = """
        <input type="hidden" name="csrfmiddlewaretoken" value="%s" id="csrftip" />
        <script src="%sbackfire/js/config.js"></script>
        <script src="%sbackfire/js/backfire-1.0.js"></script>
    """ % ( get_token(request), settings.STATIC_URL, settings.STATIC_URL )

                content = response.content
                index = content.find('</body>')
                if index == -1: return response
                response.content = content[:index] + html + content[index:]
        except Exception:
            pass
        return response
